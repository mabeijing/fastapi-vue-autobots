from pydantic import BaseModel, constr


class CompanyModel(BaseModel):
    id: int
    public_key: constr(max_length=20)
    # name: constr(max_length=63)
    domains: list[constr(max_length=255)]

    class Config:
        orm_mode = True

        
