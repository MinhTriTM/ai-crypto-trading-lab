"""Accounts routes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.portfolio.virtual_account import VirtualAccount
from src.storage.repositories.account_repository import AccountRepository

router = APIRouter()
repo = AccountRepository()

class CreateAccountReq(BaseModel):
    initial_balance: float = 1000.0
    target: float = 10000.0

@router.post("/")
async def create_account(req: CreateAccountReq):
    acc = VirtualAccount(initial_balance=req.initial_balance, target=req.target)
    repo.save(acc)
    return acc.to_dict()

@router.get("/")
async def list_accounts():
    return [a.to_dict() for a in repo.list_all()]

@router.get("/{account_id}")
async def get_account(account_id: str):
    acc = repo.get(account_id)
    if not acc:
        raise HTTPException(404, "Account not found")
    return acc.to_dict()

@router.get("/{account_id}/trades")
async def get_trades(account_id: str):
    acc = repo.get(account_id)
    if not acc:
        raise HTTPException(404, "Account not found")
    return [t.__dict__ for t in acc.trades]

@router.delete("/{account_id}")
async def delete_account(account_id: str):
    # mock
    return {"deleted": account_id}
