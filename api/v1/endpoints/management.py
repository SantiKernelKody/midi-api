from datetime import datetime
from math import ceil
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional
from models.caretaker_player import CaretakerPlayer
from models.educational_entity import EducationalEntity as EducationalEntityModel  # Renombrado para evitar confusión
from schemas.educational_entity import EducationalEntityCreate, EducationalEntityUpdate, EducationalEntity as EducationalEntitySchema
from db.session import get_db
from utils.jwt_helper import get_current_user, create_access_token
from models.dashboard_user import DashboardUser as DashboardUserModel
from schemas.dashboard_user import DashboardUserCreate, DashboardUser as DashboardUserSchema
from utils.email import send_signup_email 
from models.user_role import UserRole as UserRoleModel
from schemas.course import CourseBase, CourseCreate, CourseUpdate, Course as CourseSchema 
from models.course import Course as CourseModel
from models.player import Player as PlayerModel
from models.course_player import CoursePlayer

from schemas.player import Player as PlayerSchema, PlayerCreate, PlayerDetailSchema, PlayerUpdate, PlayerWithCaretaker
from models.education_reviewer import EducationReviewer as EducationReviewerModel

from crud.user_role import get_parent_role_id, is_admin, is_teacher

router = APIRouter()

@router.get("/get_schools", response_model=Dict[str, Any])
def get_schools(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    offset = (page - 1) * size

    if is_admin(current_user, db):
        # Si es admin, devolver todas las escuelas
        total_items = db.query(EducationalEntityModel).count()
        schools = db.query(EducationalEntityModel).offset(offset).limit(size).all()
    elif is_teacher(current_user, db):
        # Si es teacher, devolver solo las escuelas con las que está asociado
        total_items = db.query(EducationalEntityModel)\
            .join(EducationReviewerModel, EducationReviewerModel.education_id == EducationalEntityModel.id)\
            .filter(EducationReviewerModel.reviewer_id == current_user.id).count()

        schools = db.query(EducationalEntityModel)\
            .join(EducationReviewerModel, EducationReviewerModel.education_id == EducationalEntityModel.id)\
            .filter(EducationReviewerModel.reviewer_id == current_user.id).offset(offset).limit(size).all()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to access schools")

    total_pages = (total_items + size - 1) // size

    school_schemas = [EducationalEntitySchema.from_orm(school) for school in schools]

    return {
        "schools": school_schemas,
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }

@router.get("/get_school/{school_id}", response_model=EducationalEntitySchema)
def get_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    # Verificar que el usuario sea admin o teacher
    if not (is_admin(current_user, db) or is_teacher(current_user, db)):
        raise HTTPException(status_code=403, detail="Not authorized to access school information")

    # Buscar la escuela por ID
    school = db.query(EducationalEntityModel).filter(EducationalEntityModel.id == school_id).first()

    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    return school


@router.post("/create_school")
def create_school(
    school_data: EducationalEntityCreate,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to create schools")
    
    # Asigna la fecha de creación si no está configurada
    new_school = EducationalEntityModel(
        **school_data.dict(),
        created_at=datetime.utcnow()  # Asegura que `created_at` no sea None
    )
    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    
    return new_school

@router.put("/edit_school/{school_id}", response_model=EducationalEntitySchema)
def edit_school(
    school_id: int,
    school_data: EducationalEntityUpdate,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to edit schools")
    
    school = db.query(EducationalEntityModel).filter(EducationalEntityModel.id == school_id).first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    for key, value in school_data.dict(exclude_unset=True).items():
        setattr(school, key, value)
    
    db.commit()
    db.refresh(school)
    
    return school

@router.delete("/delete_school/{school_id}")
def delete_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to delete schools")
    
    school = db.query(EducationalEntityModel).filter(EducationalEntityModel.id == school_id).first()
    
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    db.delete(school)
    db.commit()
    
    return {"message": "School deleted successfully"}


@router.get("/get_teachers/{school_id}", response_model=dict)
def get_teachers(
    school_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to access teachers")

    offset = (page - 1) * size

    # Contar el número total de profesores en la escuela especificada
    total_items = db.query(DashboardUserModel).join(EducationReviewerModel, EducationReviewerModel.reviewer_id == DashboardUserModel.id)\
        .filter(DashboardUserModel.role_id == 2, EducationReviewerModel.education_id == school_id).count()

    # Obtener los profesores con paginación
    teachers = db.query(DashboardUserModel).join(EducationReviewerModel, EducationReviewerModel.reviewer_id == DashboardUserModel.id)\
        .filter(DashboardUserModel.role_id == 2, EducationReviewerModel.education_id == school_id)\
        .offset(offset).limit(size).all()

    # Convertir los profesores a esquemas
    teachers_schemas = [DashboardUserSchema.from_orm(teacher) for teacher in teachers]

    # Calcular el total de páginas
    total_pages = (total_items // size) + (1 if total_items % size != 0 else 0)

    return {
        "teachers": teachers_schemas,
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }


@router.post("/create_teacher", response_model=DashboardUserSchema)
def create_teacher(
    teacher_data: DashboardUserCreate,
    school_id: int,  # Agregar school_id como parámetro
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to create teachers")
    
    # Verificar si el email ya existe
    existing_user = db.query(DashboardUserModel).filter(DashboardUserModel.email == teacher_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    # Obtener el role_id del rol "teacher"
    role = db.query(UserRoleModel).filter(UserRoleModel.name == "teacher").first()
    if not role:
        raise HTTPException(status_code=404, detail="Role 'teacher' not found")
    role_id = role.id

    # Crear el teacher en la base de datos sin contraseña
    new_teacher = DashboardUserModel(
        email=teacher_data.email,  # Asumiendo que user_name es el correo electrónico
        name=teacher_data.name,
        last_name=teacher_data.last_name,
        role_id=role_id  # Rol de teacher
    )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    # Crear la asociación en la tabla education_reviewer
    education_reviewer = EducationReviewerModel(
        education_id=school_id,
        reviewer_id=new_teacher.id
    )
    db.add(education_reviewer)
    db.commit()

    # Crear token de acceso para el registro
    signup_token = create_access_token(user_id=new_teacher.id, role_id=new_teacher.role_id)
    
    # Enviar correo de signup
    background_tasks.add_task(
        send_signup_email,
        new_teacher.email,
        "Maestro",
        signup_token
    )
    
    return new_teacher




@router.delete("/delete_teacher/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to delete teachers")
    
    teacher = db.query(DashboardUserModel).filter(DashboardUserModel.id == teacher_id, DashboardUserModel.role_id == 2).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    db.delete(teacher)
    db.commit()
    
    return {"message": "Teacher deleted successfully"}

@router.get("/get_courses/{school_id}", response_model=dict)
def get_courses(
    school_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    offset = (page - 1) * size

    if is_admin(current_user, db):
        # Si es admin, contar todos los cursos de la escuela especificada
        total_items = db.query(CourseModel).filter(CourseModel.school_id == school_id).count()
        # Obtener cursos con paginación
        courses = db.query(CourseModel).filter(CourseModel.school_id == school_id).offset(offset).limit(size).all()
    elif is_teacher(current_user, db):
        # Si es teacher, contar solo los cursos que creó en la escuela especificada
        total_items = db.query(CourseModel).filter(
            CourseModel.school_id == school_id,
            CourseModel.reviewer_id == current_user.id
        ).count()
        # Obtener cursos con paginación
        courses = db.query(CourseModel).filter(
            CourseModel.school_id == school_id,
            CourseModel.reviewer_id == current_user.id
        ).offset(offset).limit(size).all()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to access courses")

    # Convertir los cursos a esquemas
    courses_schemas = [CourseSchema.from_orm(course) for course in courses]

    # Calcular el total de páginas
    total_pages = (total_items // size) + (1 if total_items % size != 0 else 0)

    return {
        "courses": courses_schemas,
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }


@router.get("/get_course/{course_id}", response_model=CourseSchema)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    # Buscar el curso por ID
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Verificar permisos
    if not (is_admin(current_user, db) or (is_teacher(current_user, db) and course.reviewer_id == current_user.id)):
        raise HTTPException(status_code=403, detail="Not authorized to access this course")

    return course

@router.post("/create_course/{school_id}", response_model=CourseSchema)
def create_course(
    school_id: int,
    course_data: CourseBase,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to create courses")
    
    # Verificar que el school_id exista
    school = db.query(EducationalEntityModel).filter(EducationalEntityModel.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    # Crear el curso asociado a la escuela y al teacher
    new_course = CourseModel(
        subject_name=course_data.subject_name,
        description=course_data.description,
        school_id=school_id,
        reviewer_id=current_user.id  # Se asume que el reviewer_id es el ID del usuario actual (teacher)
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@router.put("/edit_course/{course_id}", response_model=CourseSchema)
def edit_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to edit courses")
    
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Permitir que solo el creador del curso o un administrador pueda editar
    if current_user.role.name == 'teacher' and course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this course")

    for key, value in course_data.dict(exclude_unset=True).items():
        setattr(course, key, value)
    
    db.commit()
    db.refresh(course)

    return course

@router.get("/get_kids/{course_id}", response_model=Dict[str, Any])
def get_kids(
    course_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to access kids")

    offset = (page - 1) * size

    # Obtener el total de niños asociados al curso dado (sin paginación)
    total_items = db.query(PlayerModel).join(CoursePlayer).filter(CoursePlayer.course_id == course_id).count()

    if total_items == 0:
        return {
            "kids": [],
            "total_items": 0,
            "page": page,
            "size": size,
            "total_pages": 0
        }

    # Obtener los niños asociados al curso dado con paginación
    kids = (
        db.query(PlayerModel)
        .join(CoursePlayer, CoursePlayer.player_id == PlayerModel.id)
        .filter(CoursePlayer.course_id == course_id)
        .offset(offset)
        .limit(size)
        .all()
    )

    # Convertir la lista de objetos `PlayerModel` a una lista de esquemas `PlayerSchema`
    kids_schemas = [PlayerSchema.from_orm(kid) for kid in kids]

    total_pages = ceil(total_items / size)

    return {
        "kids": kids_schemas,
        "total_items": total_items,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }

@router.get("/get_player_info/{player_id}", response_model=PlayerDetailSchema)
def get_player_info(
    player_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    # Verificar si el usuario tiene permiso para acceder a la información del niño
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to access player information")

    # Obtener la información del niño
    player = db.query(PlayerModel).filter(PlayerModel.id == player_id).first()
    
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Obtener la información del parent asociado usando la tabla caretaker_player
    caretaker = (
        db.query(DashboardUserModel)
        .join(CaretakerPlayer, CaretakerPlayer.representative_id == DashboardUserModel.id)
        .filter(CaretakerPlayer.player_id == player_id)
        .first()
    )
    
    player_detail = {
        "full_name": player.full_name,
        "edad": player.edad,
        "ethnicity": player.ethnicity,
        "caretaker_name": caretaker.name if caretaker else "No asignado",
        "caretaker_email": caretaker.email if caretaker else "No asignado"
    }

    return player_detail


@router.post("/create_kid/{course_id}", response_model=PlayerSchema)
def create_kid(
    course_id: int,
    kid_data: PlayerWithCaretaker,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to create kids")
    
    new_parent = None
    if kid_data.caretaker_email:
        # Verificar si el email del padre ya existe
        existing_parent = db.query(DashboardUserModel).filter(DashboardUserModel.email == kid_data.caretaker_email).first()
        
        if not existing_parent:
            # Crear el padre en la base de datos sin contraseña
            role_id = get_parent_role_id(db)
            new_parent = DashboardUserModel(
                email=kid_data.caretaker_email,
                role_id=role_id,
                name="[Pending]",  # Puedes solicitar o recibir el nombre real del padre
                last_name=""  # Puedes solicitar o recibir el apellido real del padre
            )
            db.add(new_parent)
            db.commit()
            db.refresh(new_parent)

            # Crear token de acceso para el registro
            signup_token = create_access_token(user_id=new_parent.id, role_id=new_parent.role_id)
            
            # Enviar correo de signup
            background_tasks.add_task(
                send_signup_email,
                new_parent.email,
                "Padre de familia",
                signup_token
            )
        else:
            new_parent = existing_parent
    
    # Crear el niño
    new_kid = PlayerModel(
        full_name=kid_data.full_name,
        edad=kid_data.edad,
        ethnicity=kid_data.ethnicity,
    )
    db.add(new_kid)
    db.commit()
    db.refresh(new_kid)
    
    # Asociar el niño con el curso
    course_player = CoursePlayer(
        course_id=course_id,
        player_id=new_kid.id
    )
    db.add(course_player)

    # Asociar el niño con el cuidador si se proporcionó un correo de cuidador
    if new_parent:
        caretaker_association = CaretakerPlayer(
            representative_id=new_parent.id,
            player_id=new_kid.id
        )
        db.add(caretaker_association)
    
    db.commit()

    return new_kid




@router.put("/edit_kid/{kid_id}")
def edit_kid(
    kid_id: int,
    kid_data: PlayerWithCaretaker,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to edit kids")
    
    kid = db.query(PlayerModel).filter(PlayerModel.id == kid_id).first()
    
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")

    # Update kid's data
    for key, value in kid_data.dict(exclude_unset=True).items():
        if key != "caretaker_email":
            setattr(kid, key, value)

    # Handle caretaker email if provided
    if kid_data.caretaker_email:
        print("Si se recibio el email del cuidador")
        # Validate email format
        new_caretaker_email = kid_data.caretaker_email

        # Check if the player already has a caretaker and remove the old association
        old_caretaker = db.query(CaretakerPlayer).filter(CaretakerPlayer.player_id == kid_id).first()
        if old_caretaker:
            print("Si se encontro un cuidador antiguo")
            db.delete(old_caretaker)
            db.commit()

        # Check if the new caretaker email exists
        caretaker = db.query(DashboardUserModel).filter(
            DashboardUserModel.email == new_caretaker_email, 
            DashboardUserModel.role_id == get_parent_role_id(db)  # Assuming PARENT_ROLE_ID is defined elsewhere
        ).first()

        if not caretaker:
            print("Si se encontro que el correo que se recibio ya tiene una cuenta creada ya")
            # Create a new caretaker user
            caretaker = DashboardUserModel(
                email=new_caretaker_email,
                role_id=get_parent_role_id(db),
                name="[Pending]",  # You may request the real name from the parent
                last_name=""  # You may request the real last name from the parent
            )
            db.add(caretaker)
            db.commit()
            db.refresh(caretaker)

            # Send signup email
            signup_token = create_access_token(user_id=caretaker.id, role_id=caretaker.role_id)
            background_tasks.add_task(
                send_signup_email,
                caretaker.email,
                "Parent",
                signup_token
            )

        # Associate the new caretaker with the player
        new_caretaker_association = CaretakerPlayer(
            representative_id=caretaker.id,
            player_id=kid_id
        )
        db.add(new_caretaker_association)
    
    db.commit()
    
    return {"message": "Kid updated successfully"}



@router.delete("/delete_kid/{kid_id}")
def delete_kid(
    kid_id: int,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to delete kids")
    
    kid = db.query(PlayerModel).filter(PlayerModel.id == kid_id).first()
    
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")
    
    db.delete(kid)
    db.commit()
    
    return {"message": "Kid deleted successfully"}
