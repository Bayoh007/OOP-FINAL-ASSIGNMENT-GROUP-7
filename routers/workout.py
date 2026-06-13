@router.post("/")
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db)
):

    new_workout = Workout(
        workout_name=workout.workout_name,
        duration=workout.duration,
        calories_burned=workout.calories_burned,
        user_id=1
    )

    db.add(new_workout)

    db.commit()

    db.refresh(new_workout)

    return new_workout

@router.get("/")
def get_workouts(
    db: Session = Depends(get_db)
):
    return db.query(Workout).all()

@router.get("/{workout_id}")
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db)
):

    workout = db.query(Workout).filter(
        Workout.id == workout_id
    ).first()

    return workout