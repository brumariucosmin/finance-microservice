from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.finance import (
    LoanRequest, LoanResponse,
    CompoundInterestRequest, CompoundInterestResponse,
    NPVRequest, NPVResponse,
    IRRRequest, IRRResponse,
)
from app.services.finance import calculate_loan, compound_interest, npv, irr
from app.core.database import SessionLocal
from app.models.request_log import RequestLog

router = APIRouter(prefix="/finance", tags=["finance"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/loan", response_model=LoanResponse)
def loan_endpoint(req: LoanRequest, db: Session = Depends(get_db)):
    payment, total = calculate_loan(**req.dict())
    db.add(RequestLog(operation="loan", params=req.dict()))
    db.commit()
    return LoanResponse(payment=payment, total=total)


@router.post("/compound-interest", response_model=CompoundInterestResponse)
def ci_endpoint(req: CompoundInterestRequest, db: Session = Depends(get_db)):
    fv = compound_interest(**req.dict())
    db.add(RequestLog(operation="compound-interest", params=req.dict()))
    db.commit()
    return CompoundInterestResponse(future_value=fv)


@router.post("/npv", response_model=NPVResponse)
def npv_endpoint(req: NPVRequest, db: Session = Depends(get_db)):
    result = npv(req.rate, req.cash_flows)
    db.add(RequestLog(operation="npv", params=req.dict()))
    db.commit()
    return NPVResponse(npv=result)


@router.post("/irr", response_model=IRRResponse)
def irr_endpoint(req: IRRRequest, db: Session = Depends(get_db)):
    result = irr(req.cash_flows)
    db.add(RequestLog(operation="irr", params=req.dict()))
    db.commit()
    return IRRResponse(irr=result)
