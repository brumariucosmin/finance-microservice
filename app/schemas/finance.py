from pydantic import BaseModel, Field

from typing import List


class LoanRequest(BaseModel):
    principal: float = Field(
        ...,
        gt=0,
        description="Suma împrumutată",
    )
    annual_rate: float = Field(
        ...,
        ge=0,
        description="Rata anuală (%)",
    )
    years: int = Field(
        ...,
        gt=0,
        description="Număr de ani",
    )
    payments_per_year: int = Field(
        12,
        gt=0,
        description="Plăți pe an",
    )


class LoanResponse(BaseModel):
    payment: float = Field(
        ...,
        description="Plata per perioadă",
    )
    total: float = Field(
        ...,
        description="Suma totală plătită",
    )


class CompoundInterestRequest(BaseModel):
    principal: float = Field(
        ...,
        gt=0,
        description="Principal",
    )
    annual_rate: float = Field(
        ...,
        ge=0,
        description="Rata anuală (%)",
    )
    periods_per_year: int = Field(
        ...,
        gt=0,
        description="Număr de perioade/an",
    )
    years: float = Field(
        ...,
        ge=0,
        description="Număr de ani",
    )


class CompoundInterestResponse(BaseModel):
    future_value: float = Field(
        ...,
        description="Valoarea viitoare",
    )


class NPVRequest(BaseModel):
    rate: float = Field(
        ...,
        ge=0,
        le=1,
        description="Rata de actualizare (ex. 0.05 pentru 5%)",
    )
    cash_flows: List[float] = Field(
        ...,
        description="Lista de cash-flow-uri (pozitive/negative)",
    )


class NPVResponse(BaseModel):
    npv: float = Field(
        ...,
        description="Valoarea actuală netă",
    )


class IRRRequest(BaseModel):
    cash_flows: List[float] = Field(
        ...,
        description="Lista de cash-flow-uri pentru calcul IRR",
    )


class IRRResponse(BaseModel):
    irr: float = Field(
        ...,
        description="Internal Rate of Return",
    )
