from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from models.educational_entity import EducationalEntity as EducationalEntityModel  # Renombrado para evitar confusión
from schemas.educational_entity import EducationalEntityCreate, EducationalEntityUpdate, EducationalEntity as EducationalEntitySchema
from db.session import get_db
from utils.jwt_helper import get_current_user, create_access_token
from models.dashboard_user import DashboardUser as DashboardUserModel
from schemas.dashboard_user import DashboardUserCreate, DashboardUser as DashboardUserSchema
from utils.email import send_signup_email 
from models.user_role import UserRole as UserRoleModel
from schemas.course import CourseCreate, CourseUpdate, Course as CourseSchema 
from models.course import Course as CourseModel
from models.player import Player as PlayerModel
from models.course_player import CoursePlayer

from schemas.player import Player as PlayerSchema, PlayerCreate, PlayerUpdate
from models.education_reviewer import EducationReviewer as EducationReviewerModel

from crud.user_role import is_admin, is_teacher

router = APIRouter()

@router.get("/get_schools", response_model=List[EducationalEntitySchema])
def get_schools(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    offset = (page - 1) * size
    
    if is_admin(current_user, db):
        # Si es admin, devolver todas las escuelas
        schools = db.query(EducationalEntityModel).offset(offset).limit(size).all()
    elif is_teacher(current_user, db):
        # Si es teacher, devolver solo las escuelas con las que está asociado
        schools = db.query(EducationalEntityModel)\
            .join(EducationReviewerModel, EducationReviewerModel.education_id == EducationalEntityModel.id)\
            .filter(EducationReviewerModel.reviewer_id == current_user.id).offset(offset).limit(size).all()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to access schools")

    return schools

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


@router.get("/get_teachers/{school_id}", response_model=List[DashboardUserSchema])
def get_teachers(
    school_id: int,  # No necesita `Path(...)`
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to access teachers")

    offset = (page - 1) * size

    # Filtrar profesores por la escuela especificada
    teachers = db.query(DashboardUserModel).join(EducationReviewerModel, EducationReviewerModel.reviewer_id == DashboardUserModel.id)\
        .filter(DashboardUserModel.role_id == 2, EducationReviewerModel.education_id == school_id)\
        .offset(offset).limit(size).all()

    return teachers

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

@router.get("/get_courses/{school_id}", response_model=List[CourseSchema])
def get_courses(
    school_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    offset = (page - 1) * size

    if is_admin(current_user, db):
        # Si es admin, devolver todos los cursos de la escuela especificada
        courses = db.query(CourseModel).filter(CourseModel.school_id == school_id).offset(offset).limit(size).all()
    elif is_teacher(current_user, db):
        # Si es teacher, devolver solo los cursos que creó en la escuela especificada
        courses = db.query(CourseModel).filter(
            CourseModel.school_id == school_id,
            CourseModel.reviewer_id == current_user.id
        ).offset(offset).limit(size).all()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to access courses")

    return courses

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
    if not (is_admin(current_user, db) or (is_teacher(current_user, db) and course.teacher_id == current_user.id)):
        raise HTTPException(status_code=403, detail="Not authorized to access this course")

    return course

@router.post("/create_course/{school_id}", response_model=CourseSchema)
def create_course(
    school_id: int,
    course_data: CourseCreate,
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

@router.get("/get_kids/{course_id}", response_model=List[PlayerSchema])
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
    
    # Filtrar los niños asociados al curso dado
    kids = (
        db.query(PlayerModel)
        .join(CoursePlayer, CoursePlayer.player_id == PlayerModel.id)
        .filter(CoursePlayer.course_id == course_id)
        .offset(offset)
        .limit(size)
        .all()
    )

    if not kids:
        raise HTTPException(status_code=404, detail="No kids found for the given course")

    return kids

@router.post("/create_kid/{course_id}", response_model=PlayerSchema)
def create_kid(
    course_id: int,
    kid_data: PlayerCreate,
    parent_email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to create kids")
    
    # Verificar si el email del padre ya existe
    existing_parent = db.query(DashboardUserModel).filter(DashboardUserModel.email == parent_email).first()
    
    if not existing_parent:
        # Crear el padre en la base de datos sin contraseña
        role_id = db.query(UserRoleModel).filter(UserRoleModel.name == "parent").first().id
        new_parent = DashboardUserModel(
            email=parent_email,
            role_id=role_id,
            name="[Pendiente]",  # Puedes solicitar o recibir el nombre real del padre
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
    
    # Crear el niño y asociarlo con el padre
    new_kid = PlayerModel(
        full_name=kid_data.full_name,
        edad=kid_data.edad,
        ethnicity=kid_data.ethnicity,
        caretaker_id=new_parent.id  # Asociar con el padre creado o existente
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
    db.commit()

    return new_kid


@router.put("/edit_kid/{kid_id}")
def edit_kid(
    kid_id: int,
    kid_data: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: DashboardUserModel = Depends(get_current_user)
):
    if not is_admin(current_user, db) and not is_teacher(current_user, db):
        raise HTTPException(status_code=403, detail="Not authorized to edit kids")
    
    kid = db.query(PlayerModel).filter(PlayerModel.id == kid_id).first()
    
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")
    
    for key, value in kid_data.dict().items():
        setattr(kid, key, value)
    
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
