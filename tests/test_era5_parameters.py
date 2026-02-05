from dataclasses import asdict

from pjenergy.era5.parameters import ERA5Parameters


def sample_data():
    return {
        "dataset": "ds",
        "product_type": ["a", "b"],
        "variable": ["v1"],
        "year": ["2020", "2021"],
        "month": ["01"],
        "day": ["01", "02", "03"],
        "time": ["00:00", "01:00"],
        "area": [1, 2, 3, 4],
        "pressure_level": ["1000", "925"],
        "data_format": ["netcdf"],
        "download_format": ["unarchived"],
    }


def test_to_cds_dict_removes_dataset():
    data = sample_data()
    params = ERA5Parameters(**data)
    cds_dict = params.to_cds_dict()
    expected = asdict(params)
    expected.pop("dataset")
    assert cds_dict == expected
    assert "dataset" not in cds_dict


def test_count_parameter_combinations_ignores_area():
    data = sample_data()
    assert ERA5Parameters.count_parameter_combinations(data) == 48


def test_is_splitting_invalid():
    data = {"year": ["2020"], "month": ["01", "02"], "day": "01"}
    assert ERA5Parameters._is_splitting_invalid(data, "year") is True
    assert ERA5Parameters._is_splitting_invalid(data, "day") is True
    assert ERA5Parameters._is_splitting_invalid(data, "month") is False


def test_fix_parameter():
    data = {"month": ["01", "02"]}
    fixed = ERA5Parameters._fix_parameter(data, "month", 1)
    assert fixed["month"] == "02"
    assert data["month"] == ["01", "02"]

    data_single = {"year": ["2020"]}
    assert ERA5Parameters._fix_parameter(data_single, "year", 0) is data_single


def test_brake_depth_respects_limit():
    data = sample_data()
    assert ERA5Parameters.brake_depth(data, 1000) == 0
    assert ERA5Parameters.brake_depth(data, 10) == 3


def test_separates_one_parameter_values():
    data = {"year": ["2020", "2021", "2022"]}
    split = ERA5Parameters.separates_one_parameter_values(data, "year")
    assert [d["year"] for d in split] == ["2020", "2021", "2022"]


def test_separates_parameters_values():
    data = {"year": ["2020", "2021"], "month": ["01", "02"]}
    split = ERA5Parameters.separates_parameters_values(data, 2)
    assert len(split) == 4
    assert {d["year"] for d in split} == {"2020", "2021"}
    assert {d["month"] for d in split} == {"01", "02"}
