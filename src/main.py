import os
import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, Relationship, select
from sqlalchemy import CHAR

class MaterialBase(SQLModel):
    id: str = Field(primary_key=True, sa_type=CHAR(7))
    name: str = Field(index=True, min_length=1)

class MaterialCreate(MaterialBase):
    pass

class Material(MaterialBase, table=True):
    __tablename__ = "materials"

    inbounds: list["Inbound"] = Relationship(back_populates="material")

class InboundBase(SQLModel):
    #Note: 0より大きい値のみ許可する
    quantity: int = Field(gt=0)
    # 外部キー
    material_id: str = Field(foreign_key="materials.id")

class InboundCreate(InboundBase):
    pass

class Inbound(InboundBase, table=True):
    __tablename__ = "inbounds"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # 親ヘの参照
    material: Material = Relationship(back_populates="inbounds")

DATABASE_URI = os.environ.get("DATABASE_URL")
engine = create_engine(url=DATABASE_URI, echo=True)

def create_db_and_tables():
    """データベースとテーブルを作成する"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """データベースセッションを取得する"""
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """アプリケーション起動時の初期化処理を行う"""
    create_db_and_tables()

@app.post("/inbounds/", response_model=Inbound)
def create_inbound(*, session: Session = Depends(get_session), inbound: InboundCreate):
    """
    入荷情報を登録する
    """
    db_inbound = Inbound.model_validate(inbound)
    session.add(db_inbound)
    session.commit()
    session.refresh(db_inbound)
    return db_inbound

@app.post("/materials/", response_model=Material)
def create_material(*, session: Session = Depends(get_session), material: MaterialCreate):
    """
    資材情報を登録する
    """
    db_material = Material.model_validate(material)
    session.add(db_material)
    session.commit()
    session.refresh(db_material)
    return db_material

@app.get("/materials/", response_model=list[Material])
def get_materials(*, session: Session = Depends(get_session)):
    """
    全ての資材情報を取得する
    """
    materials = session.exec(select(Material)).all()
    return materials

@app.get("/materials/{material_id}", response_model=Material)
def get_material_name_by_id(*, session: Session = Depends(get_session), material_id: str):
    """
    指定されたIDの資材情報を取得する
    """
    target_material = session.exec(select(Material).where(Material.id == material_id)).first()
    return target_material

@app.get("/inbounds/", response_model=list[Inbound])
def get_inbounds(*, session: Session = Depends(get_session)):
    """
    全ての入荷情報を取得する
    """
    inbounds = session.exec(select(Inbound)).all()

@app.get("/inbounds/{inbound_id}", response_model=Inbound)
def get_inbound_by_id(*, session: Session = Depends(get_session), inbound_id: str):
    """
    指定されたIDの入荷情報を取得する
    """
    target_inbound = session.exec(select(Inbound).where(Inbound.id == inbound_id)).first()
    return target_inbound