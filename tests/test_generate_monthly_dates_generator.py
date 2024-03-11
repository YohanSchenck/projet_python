from moulinette.extract import generate_monthly_dates_generator


def test_generate_monthly_dates_generator():
    dates = list(generate_monthly_dates_generator("202001", "202003"))
    assert dates == ["202001", "202002", "202003"]
