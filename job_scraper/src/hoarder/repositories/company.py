from typing import Optional
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.hoarder.models import Company


class CompanyRepository:
    """Repository for Company model operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, industry: Optional[str] = None) -> Company:
        """Create a new company"""
        company = Company(name=name, industry=industry)
        self.session.add(company)
        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def get_by_id(self, company_id: int) -> Optional[Company]:
        """Get a company by ID"""
        res = await self.session.execute(select(Company).filter(Company.id == company_id))
        return res.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Company]:
        """Get a company by name (case-insensitive)"""
        res = await self.session.execute(
            select(Company).filter(func.lower(Company.name) == func.lower(name))
        )
        return res.scalar_one_or_none()

    async def get_all(self) -> list[Company]:
        """Get all companies"""
        res = await self.session.execute(select(Company))
        return list(res.scalars().all())

    async def get_or_create(self, name: str, industry: Optional[str] = None) -> Company:
        """Get a company by name (case-insensitive) or create if it doesn't exist"""
        company = await self.get_by_name(name)
        if not company:
            company = await self.create(name, industry)
        return company

    async def update(
        self,
        company_id: int,
        name: Optional[str] = None,
        industry: Optional[str] = None,
    ) -> Optional[Company]:
        """Update a company"""
        company = await self.get_by_id(company_id)
        if not company:
            return None

        if name is not None:
            company.name = name
        if industry is not None:
            company.industry = industry

        await self.session.commit()
        await self.session.refresh(company)
        return company

    async def delete(self, company_id: int) -> bool:
        """Delete a company by ID"""
        company = await self.get_by_id(company_id)
        if not company:
            return False

        await self.session.delete(company)
        await self.session.commit()
        return True
