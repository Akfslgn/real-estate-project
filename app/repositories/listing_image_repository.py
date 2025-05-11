from typing import Optional, List
from app.extensions import db
from app.models.listing_image import ListingImage
from sqlalchemy import select


class ListingImageRepository:
    @staticmethod
    def create(listing_id: int, image_url: str, cl_pid: str, **kwargs) -> ListingImage:
        image = ListingImage(listing_id=listing_id,
                             image_url=image_url, claudinary_public_id=cl_pid)
        for key, value in kwargs.items():
            if hasattr(image, key):
                setattr(image, key, value)
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def get_by_id(image_id: int) -> Optional[ListingImage]:
        """Get image by ID"""
        stmnt = select(ListingImage).where(
            ListingImage.id == image_id)
        result = db.session.execute(stmnt)
        return result.scalars().first()

    @staticmethod
    def get_by_listing_id(listing_id: int) -> List[ListingImage]:
        """Get image by listing ID"""
        stmnt = select(ListingImage).where(
            ListingImage.listing_id == listing_id)
        result = db.session.execute(stmnt)
        return List(result.scalars().all())

    @staticmethod
    def get_primary_image(listing_id: int) -> Optional[ListingImage]:
        """Get primary image by listing ID"""
        stmnt = select(ListingImage).where(
            ListingImage.listing_id == listing_id, ListingImage.is_primary == True)
        result = db.session.execute(stmnt)
        return result.scalars().first()

    @staticmethod
    def delete(image: ListingImage) -> bool:
        """Delete the image"""
        db.session.delete(image)
        db.session.commit()
        return True

    @staticmethod
    def update(image: ListingImage) -> ListingImage:
        """Update the image"""
        db.session.commit()
        return image
