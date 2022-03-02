def get_calories(weight, duration):
    # 식 : MET(요가 에너지소비량) x Weight(몸무게)  x 0.0175 x Time(min) = Kcal
    return 3.1 * weight * 0.0175 * duration
