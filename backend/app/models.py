import enum
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


class Perfil(str, enum.Enum):
    necesita_cuidado = "necesita_cuidado"
    puede_cuidar = "puede_cuidar"
    organizacion = "organizacion"


class TipoCuidado(str, enum.Enum):
    acompanamiento = "acompanamiento"
    apoyo_hogar = "apoyo_hogar"
    comidas = "comidas"
    traslados = "traslados"
    cuidado_nocturno = "cuidado_nocturno"


class EstadoSolicitud(str, enum.Enum):
    abierta = "abierta"
    cerrada = "cerrada"
    cancelada = "cancelada"


class Usuario(Base):
    """Persona que usa la plataforma. La zona se guarda como AGEB, nunca como dirección exacta."""

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[str] = mapped_column(String(120))
    perfil: Mapped[Perfil] = mapped_column(Enum(Perfil))
    ageb: Mapped[str | None] = mapped_column(String(20), nullable=True)
    acepto_aviso_privacidad: Mapped[bool]
    fecha_consentimiento: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_ahora)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_ahora)

    servicios: Mapped[list["Servicio"]] = relationship(
        back_populates="persona_cuidadora", cascade="all, delete-orphan"
    )
    solicitudes: Mapped[list["Solicitud"]] = relationship(
        back_populates="solicitante", cascade="all, delete-orphan"
    )


class Servicio(Base):
    """Servicio que ofrece una persona cuidadora, con su rango de tarifa por hora (MXN)."""

    __tablename__ = "servicios"
    __table_args__ = (
        CheckConstraint("tarifa_min >= 0", name="ck_servicio_tarifa_min_positiva"),
        CheckConstraint("tarifa_max >= tarifa_min", name="ck_servicio_rango_valido"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cuidadora_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    tipo_cuidado: Mapped[TipoCuidado] = mapped_column(Enum(TipoCuidado))
    tarifa_min: Mapped[int] = mapped_column(Integer)
    tarifa_max: Mapped[int] = mapped_column(Integer)
    disponibilidad: Mapped[str | None] = mapped_column(String(200), nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_ahora)

    persona_cuidadora: Mapped["Usuario"] = relationship(back_populates="servicios")


class Solicitud(Base):
    """Necesidad de cuidado publicada por quien contrata, con su presupuesto por hora (MXN)."""

    __tablename__ = "solicitudes"
    __table_args__ = (
        CheckConstraint("presupuesto_min >= 0", name="ck_solicitud_presupuesto_min_positivo"),
        CheckConstraint("presupuesto_max >= presupuesto_min", name="ck_solicitud_rango_valido"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    solicitante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    tipo_cuidado: Mapped[TipoCuidado] = mapped_column(Enum(TipoCuidado))
    horario: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ageb: Mapped[str | None] = mapped_column(String(20), nullable=True)
    presupuesto_min: Mapped[int] = mapped_column(Integer)
    presupuesto_max: Mapped[int] = mapped_column(Integer)
    estado: Mapped[EstadoSolicitud] = mapped_column(Enum(EstadoSolicitud), default=EstadoSolicitud.abierta)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_ahora)

    solicitante: Mapped["Usuario"] = relationship(back_populates="solicitudes")
