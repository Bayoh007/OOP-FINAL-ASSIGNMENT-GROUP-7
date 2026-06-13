def calculate_bmi(
    weight: float,
    height: float
):

    bmi = weight / (height * height)

    return round(bmi, 2)