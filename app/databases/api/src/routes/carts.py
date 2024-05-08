import os
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Path
from sqlmodel import Session, select

from models.cart import Cart, CartUpdate, CartItem, CartItemUpdate
from clients.postgres import get_session

ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])


@router.post("/", response_model=Cart)
def create_cart(cart_data: Cart, session: Session = Depends(get_session)):
    session.add(cart_data)
    session.commit()
    session.refresh(cart_data)
    return cart_data


@router.get("/", response_model=List[Cart])
def read_carts(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(Cart).offset(skip).limit(limit)).all()


@router.get("/{cart_id}", response_model=Cart)
def read_cart(cart_id: int = Path(..., title="The ID of the cart to retrieve"), session: Session = Depends(get_session)):
    cart = session.get(Cart, cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.put("/{cart_id}", response_model=Cart)
def update_cart(cart_id: int, cart_data: CartUpdate, session: Session = Depends(get_session)):
    cart = session.get(Cart, cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    for field, value in cart_data.model_dump(exclude_unset=True).items():
        setattr(cart, field, value)

    session.commit()
    session.refresh(cart)

    return cart


@router.patch("/{cart_id}", response_model=Cart)
def patch_cart(cart_id: int, cart_data: CartUpdate, session: Session = Depends(get_session)):
    cart = session.get(Cart, cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")

    for field, value in cart_data.model_dump(exclude_unset=True).items():
        setattr(cart, field, value)

    session.commit()
    session.refresh(cart)

    return cart


@router.delete("/{cart_id}", response_model=Cart)
def delete_cart(cart_id: int, session: Session = Depends(get_session)):
    cart = session.get(Cart, cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    session.delete(cart)
    session.commit()
    return cart


@router.post("/{cart_id}/items", response_model=CartItem)
def create_cart_item(cart_id: int, item_data: CartItem, session: Session = Depends(get_session)):
    item_data.cart_id = cart_id
    session.add(item_data)
    session.commit()
    session.refresh(item_data)
    return item_data


@router.get("/{cart_id}/items", response_model=List[CartItem])
def read_cart_items(cart_id: int, session: Session = Depends(get_session)):
    cart_items = session.exec(select(CartItem).filter(
        CartItem.cart_id == cart_id)).all()
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart items not found")
    return cart_items


@router.get("/{cart_id}/items/{item_id}", response_model=CartItem)
def read_cart_item(cart_id: int, item_id: int, session: Session = Depends(get_session)):
    cart_item = session.get(CartItem, item_id)
    if cart_item is None or cart_item.cart_id != cart_id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item


@router.put("/{cart_id}/items/{item_id}", response_model=CartItem)
def update_cart_item(cart_id: int, item_id: int, item_data: CartItemUpdate, session: Session = Depends(get_session)):
    cart_item = session.get(CartItem, item_id)
    if cart_item is None or cart_item.cart_id != cart_id:
        raise HTTPException(status_code=404, detail="Cart item not found")

    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(cart_item, field, value)

    session.commit()
    session.refresh(cart_item)

    return cart_item


@router.patch("/{cart_id}/items/{item_id}", response_model=CartItem)
def patch_cart_item(cart_id: int, item_id: int, item_data: CartItemUpdate, session: Session = Depends(get_session)):
    cart_item = session.get(CartItem, item_id)
    if cart_item is None or cart_item.cart_id != cart_id:
        raise HTTPException(status_code=404, detail="Cart item not found")

    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(cart_item, field, value)

    session.commit()
    session.refresh(cart_item)

    return cart_item


@router.delete("/{cart_id}/items/{item_id}", response_model=CartItem)
def delete_cart_item(cart_id: int, item_id: int, session: Session = Depends(get_session)):
    cart_item = session.get(CartItem, item_id)
    if cart_item is None or cart_item.cart_id != cart_id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    session.delete(cart_item)
    session.commit()
    return cart_item

