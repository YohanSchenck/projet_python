from moulinette.extract import monthly_dates_generator


def test_monthly_dates_generator() -> None:
    dates = list(monthly_dates_generator("202001", "202003"))
    assert dates == ["202001", "202002", "202003"]
