import pytest
from delivery_location.models import DeliveryLocation
from supplier.models import Supplier
from django.core.exceptions import ValidationError
import datetime


@pytest.fixture
def test_data():
    return [
        ('taxas', 'firstname', 'lastname', 'password', 'business name'),
        ('ed', 'edd', 'eddy', 'jawbreaker101', 'jawbreaker inc'),
    ]


@pytest.fixture
def supplier0(test_data):
    return Supplier(user_name=test_data[0][0],
                    first_name=test_data[0][1],
                    last_name=test_data[0][2],
                    password=test_data[0][3],
                    business_name=test_data[0][4],)


@pytest.fixture
def delivery_location0(supplier0):
    return DeliveryLocation(user_name=supplier0, location="Qiryat Shemona", date=datetime.date(2022, 12, 30))


@pytest.fixture
def delivery_location1(supplier0):
    return DeliveryLocation(user_name=supplier0, location="Haifa", date=datetime.date(2022, 12, 31))


class TestDeliveryLocationModel:
    @pytest.mark.django_db()
    def test_add_delivery_location(self, supplier0, delivery_location0, delivery_location1):
        supplier0.save()
        delivery_location0.add_delivery_location()
        delivery_location1.add_delivery_location()
        assert delivery_location0 in DeliveryLocation.objects.all()
        assert delivery_location1 in DeliveryLocation.objects.all()

    @pytest.mark.django_db()
    def test_delete_non_existing_delivery_location(self):
        with pytest.raises(DeliveryLocation.DoesNotExist):
            DeliveryLocation.remove_delivery_location_by_id(-1)

    @pytest.mark.django_db()
    def test_delete_delivery_location(self, supplier0, delivery_location0):
        supplier0.save()
        delivery_location0.add_delivery_location()
        assert delivery_location0 in DeliveryLocation.objects.all()
        delivery_location0.remove_delivery_location()
        assert delivery_location0 not in DeliveryLocation.objects.all()

    @pytest.mark.django_db()
    def test_filter_by_id(self, supplier0, delivery_location0):
        supplier0.save()
        delivery_location0.add_delivery_location()
        assert delivery_location0 == DeliveryLocation.get_delivery_location_by_id(delivery_location0.id)

    @pytest.mark.django_db()
    def test_filter_by_id_that_does_not_exist(self):
        with pytest.raises(DeliveryLocation.DoesNotExist):
            DeliveryLocation.get_delivery_location_by_id(-1)

    @pytest.mark.django_db()
    def test_filter_by_location_from_supplier(self, supplier0, delivery_location0):
        supplier0.save()
        delivery_location0.add_delivery_location()
        assert delivery_location0 in list(
            DeliveryLocation.filter_by_supplier_and_location(supplier0, "Qiryat Shemona"))

    @pytest.mark.django_db()
    def test_filter_by_location_that_does_not_exist_from_supplier(self, supplier0):
        supplier0.save()
        assert [] == list(DeliveryLocation.filter_by_supplier_and_location(supplier0,
                                                                           "LOCATION THAT IS NOT RELATED TO SUPPLIER0"))

    @pytest.mark.django_db()
    def test_filter_by_location(self, supplier0, delivery_location0, delivery_location1):
        supplier0.save()
        delivery_location0.add_delivery_location()
        delivery_location1.add_delivery_location()
        assert set([delivery_location0, delivery_location1]) == set(list(
            DeliveryLocation.filter_by_location(supplier0)))

    @pytest.mark.django_db()
    def test_filter_by_location_that_does_not_exist(self):
        assert [] == list(DeliveryLocation.filter_by_location("NOT EXISTED LOCATION"))

    @pytest.mark.django_db()
    def test_update_delivery_location_date(self, supplier0, delivery_location0):
        supplier0.save()
        delivery_location0.add_delivery_location()
        testnewdate = datetime.date(2023, 1, 1)
        delivery_location0.update_date(testnewdate)
        assert testnewdate == delivery_location0.date

    @pytest.mark.django_db()
    def test_update_delivery_location_location(self, supplier0, delivery_location0):
        supplier0.save()
        delivery_location0.add_delivery_location()
        delivery_location0.update_location("Yafo")
        assert "Yafo" == delivery_location0.location

    @pytest.mark.django_db()
    def test_validators(self, supplier0):
        supplier0.save()
        valtest = DeliveryLocation(user_name=supplier0, location="", date=datetime.date(2022, 12, 31))
        with pytest.raises(ValidationError):
            valtest.add_delivery_location()