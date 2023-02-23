from app.admin.schema import CompanyModel

from app.admin.models import CompanyOrm

co_orm = CompanyOrm(
    id=1,
    public_key='foobar',
    name='Testing',
    domains=['example.com', 'foobar.com'],
)

co_model = CompanyModel.from_orm(co_orm)
print(co_model)
