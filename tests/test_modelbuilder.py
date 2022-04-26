import pytest as pytest

from braincube_connector import client, modelbuilder, constants, instances
from braincube_connector.bases import base
from braincube_connector.memory_base.nested_resources.period import Period, PeriodUnitType
from braincube_connector.memory_base.nested_resources.variable import VariableDescription
from tests.mock import create_mock_var


@pytest.fixture(autouse=True)
def clean_client_instances():
    if client.INSTANCE_KEY in instances.instances:
        del instances.instances[client.INSTANCE_KEY]


def test_create_study(mocker, create_mock_var, clean_client_instances):
    mock_mb = mocker.Mock()
    mock_mb.get_bcid.return_value = "12"
    check_conf_mock = mocker.patch("os.path.exists", mocker.Mock(return_value=False))
    sso_mock = mocker.patch.object(
        client.Client, "_request_braincubes", lambda x: [base.Base("test")]
    )
    mock_add_instance = mocker.patch(
        "braincube_connector.client.instances.add_instance", side_effect=instances.add_instance
    )
    test_client = client.get_instance(
        config_dict={constants.API_KEY: "abcd", constants.DOMAIN_KEY: "mock.com"}
    )

    test = client.get_instance()
    target = create_mock_var(name="any", metadata={"standard": "name_standard", "tag": "name_tag"}, bcid="30",
                             mb=mock_mb)
    period = Period(
        begin=1650456660871,
        end=1650456660900,
        period_unit_type=PeriodUnitType.DAY,
        quantity=2,
        calendar_quantity=2,
        offset=2,
        offset_quantity=2,
    )
    variables = [
        create_mock_var(name="var1", metadata={"standard": "name_standard_1", "tag": "name_tag_1"}),
        create_mock_var(name="var2", metadata={"standard": "name_standard_2", "tag": "name_tag_2"}),
        create_mock_var(name="var3", metadata={"standard": "name_standard_3", "tag": "name_tag_3"}),
        create_mock_var(name="var4", metadata={"standard": "name_standard_4", "tag": "name_tag_4"}),
    ]
    study = test.ModelBuilder.create_study(
        name="my_study",
        description="test of a study",
        target=target,
        period=period,
        variables=variables,
    )

    assert study == "test"
