import uuid

import pytest
from model_bakery import baker

from orders.models import Order

from .helpers import compare_games, datetime_isoformats_are_close, get_json, post_json

# ==============================================================================
# ADD ORDER
# ==============================================================================


@pytest.mark.django_db
def test_add_order(client, token):
    status, response = post_json(client, '/api/orders/add/', {}, token.key)
    assert status == 200
    assert response['id'] == 1
    assert Order.objects.get(pk=1, user=token.user)


@pytest.mark.django_db
def test_add_order_fails_when_invalid_json_body(client):
    status, response = post_json(client, '/api/orders/add/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_add_order_fails_when_token_is_invalid(client):
    status, response = post_json(client, '/api/orders/add/', {}, 'invalid-token')
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
def test_add_order_fails_when_unregistered_token(client):
    status, response = post_json(client, '/api/orders/add/', {}, str(uuid.uuid4()))
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_add_order_fails_when_method_is_not_allowed(client):
    status, _ = get_json(client, '/api/orders/add/')
    assert status == 405


# ==============================================================================
# ORDER DETAIL
# ==============================================================================


@pytest.mark.django_db
def test_order_detail(client, token, order):
    order.user = token.user
    order.save()
    status, response = post_json(client, f'/api/orders/{order.pk}/', bearer_token=token.key)
    assert status == 200
    assert response['id'] == order.pk
    assert response['status'] == order.get_status_display()
    assert response['key'] is None
    for game in response['games']:
        compare_games(game, order.games.get(pk=game['id']))
    assert datetime_isoformats_are_close(response['created_at'], order.created_at.isoformat())
    assert datetime_isoformats_are_close(response['updated_at'], order.updated_at.isoformat())
    assert response['price'] == float(order.price)


@pytest.mark.django_db
def test_order_detail_fails_when_invalid_json_body(client):
    status, response = post_json(client, '/api/orders/1/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_order_detail_fails_when_invalid_token(client):
    status, response = post_json(client, '/api/orders/1/', bearer_token='invalid-token')
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
def test_order_detail_fails_when_unregistered_token(client):
    status, response = post_json(client, '/api/orders/1/', bearer_token=str(uuid.uuid4()))
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_order_detail_fails_when_user_is_not_the_owner_of_requested_order(client, token, order):
    status, response = post_json(client, f'/api/orders/{order.pk}/', bearer_token=token.key)
    assert status == 403
    assert response == {'error': 'User is not the owner of requested order'}


@pytest.mark.django_db
def test_order_detail_fails_when_order_does_not_exist(client, token):
    status, response = post_json(client, '/api/orders/1/', bearer_token=token.key)
    assert status == 404
    assert response == {'error': 'Order not found'}


@pytest.mark.django_db
def test_order_detail_fails_when_method_is_not_allowed(client):
    status, _ = get_json(client, '/api/orders/1/')
    assert status == 405


# ==============================================================================
# ORDER GAME LIST
# ==============================================================================


@pytest.mark.django_db
def test_order_game_list(client, token, order):
    order.user = token.user
    order.save()
    status, response = post_json(client, f'/api/orders/{order.pk}/games/', bearer_token=token.key)
    assert status == 200
    for game in response:
        compare_games(game, order.games.get(pk=game['id']))


@pytest.mark.django_db
def test_order_game_list_fails_when_invalid_json_body(client):
    status, response = post_json(client, '/api/orders/1/games/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_order_game_list_fails_when_invalid_token(client):
    status, response = post_json(client, '/api/orders/1/games/', bearer_token='invalid-token')
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
def test_order_game_list_when_unregistered_token(client):
    status, response = post_json(client, '/api/orders/1/games/', bearer_token=str(uuid.uuid4()))
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_order_game_list_fails_when_user_is_not_the_owner_of_requested_order(client, token, order):
    status, response = post_json(client, f'/api/orders/{order.pk}/games/', bearer_token=token.key)
    assert status == 403
    assert response == {'error': 'User is not the owner of requested order'}


@pytest.mark.django_db
def test_order_game_list_fails_when_order_does_not_exist(client, token):
    status, response = post_json(client, '/api/orders/1/games/', bearer_token=token.key)
    assert status == 404
    assert response == {'error': 'Order not found'}


@pytest.mark.django_db
def test_order_game_list_fails_when_method_is_not_allowed(client):
    status, _ = get_json(client, '/api/orders/1/games/')
    assert status == 405


# ==============================================================================
# ADD GAME TO ORDER
# ==============================================================================


@pytest.mark.django_db
def test_add_game_to_order(client, token, order, game):
    order.user = token.user
    order.save()
    status, response = post_json(
        client, f'/api/orders/{order.pk}/games/add/{game.slug}/', bearer_token=token.key
    )
    assert status == 200
    assert response['num-games-in-order'] == 1
    assert order.games.get(pk=game.pk)


@pytest.mark.django_db
def add_game_to_order_fails_when_invalid_json_body(client):
    status, response = post_json(client, '/api/orders/1/games/add/game/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def add_game_to_order_fails_when_invalid_token(client):
    status, response = post_json(
        client, '/api/orders/1/games/add/game/', bearer_token='invalid-token'
    )
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
def add_game_to_order_fails_when_game_is_out_of_stock(client, token, order, game):
    game.stock = 0
    game.save()
    order.user = token.user
    order.save()
    status, response = post_json(
        client, f'/api/orders/{order.pk}/games/add/{game.slug}/', bearer_token=token.key
    )
    assert status == 400
    assert response == {'error': 'Game is out of stock'}


@pytest.mark.django_db
def add_game_to_order_fails_when_unregistered_token(client):
    status, response = post_json(
        client, '/api/orders/1/games/add/game/', bearer_token=str(uuid.uuid4())
    )
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_add_game_to_order_fails_when_user_is_not_the_owner_of_requested_order(
    client, token, order, game
):
    status, response = post_json(
        client, f'/api/orders/{order.pk}/games/add/{game.slug}/', bearer_token=token.key
    )
    assert status == 403
    assert response == {'error': 'User is not the owner of requested order'}


@pytest.mark.django_db
def test_add_game_to_order_fails_when_order_does_not_exist(client, token):
    status, response = post_json(client, '/api/orders/1/games/add/test/', bearer_token=token.key)
    assert status == 404
    assert response == {'error': 'Order not found'}


@pytest.mark.django_db
def test_add_game_to_order_fails_when_game_does_not_exist(client, token, order):
    status, response = post_json(
        client, f'/api/orders/{order.pk}/games/add/test/', bearer_token=token.key
    )
    assert status == 404
    assert response == {'error': 'Game not found'}


@pytest.mark.django_db
def test_add_game_to_order_fails_when_method_is_not_allowed(client):
    status, _ = get_json(client, '/api/orders/1/games/add/test/')
    assert status == 405


# ==============================================================================
# CONFIRM ORDER
# ==============================================================================


@pytest.mark.django_db
def test_confirm_order(client, token, order):
    order.user = token.user
    order.save()
    status, response = post_json(client, f'/api/orders/{order.pk}/confirm/', bearer_token=token.key)
    assert status == 200
    assert response['status'] == 'Confirmed'
    assert Order.objects.get(pk=order.pk, status=Order.Status.CONFIRMED)


@pytest.mark.django_db
def test_confirm_order_fails_when_invalid_json(client):
    status, response = post_json(client, '/api/orders/1/confirm/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_confirm_order_fails_when_invalid_token(client):
    status, response = post_json(client, '/api/orders/1/confirm/', bearer_token='invalid-token')
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [Order.Status.CANCELLED, Order.Status.CONFIRMED, Order.Status.PAID]
)
def test_confirm_order_fails_when_order_is_not_initiated(client, token, order, status):
    order.user = token.user
    order.status = status
    order.save()
    status, response = post_json(client, f'/api/orders/{order.pk}/confirm/', bearer_token=token.key)
    assert status == 400
    assert response == {'error': 'Orders can only be confirmed when initiated'}


@pytest.mark.django_db
def test_confirm_order_fails_when_unregistered_token(client):
    status, response = post_json(client, '/api/orders/1/confirm/', bearer_token=str(uuid.uuid4()))
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_confirm_order_fails_when_user_is_not_the_owner_of_requested_order(client, token, order):
    status, response = post_json(client, f'/api/orders/{order.pk}/confirm/', bearer_token=token.key)
    assert status == 403
    assert response == {'error': 'User is not the owner of requested order'}


@pytest.mark.django_db
def test_confirm_order_fails_when_order_does_not_exist(client, token):
    status, response = post_json(client, '/api/orders/1/confirm/', bearer_token=token.key)
    assert status == 404
    assert response == {'error': 'Order not found'}


@pytest.mark.django_db
def test_confirm_order_fails_when_method_is_not_allowed(client):
    status, _ = get_json(client, '/api/orders/1/confirm/')
    assert status == 405


# ==============================================================================
# CANCEL ORDER
# ==============================================================================


@pytest.mark.django_db
def test_cancel_order(client, token, order):
    order.user = token.user
    order.save()
    games = baker.make('games.Game', stock=2, _fill_optional=True, _quantity=5)
    order.games.set(games)
    status, response = post_json(client, f'/api/orders/{order.pk}/cancel/', bearer_token=token.key)
    assert status == 200
    assert response['status'] == 'Cancelled'
    assert (order := Order.objects.get(pk=order.pk, status=Order.Status.CANCELLED))
    for game in order.games.all():
        assert game.stock == 3


@pytest.mark.django_db
def test_cancel_order_fails_when_invalid_json_body(client):
    status, response = post_json(client, '/api/orders/1/cancel/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_cancel_order_fails_when_invalid_token(client):
    status, response = post_json(client, '/api/orders/1/cancel/', bearer_token='invalid-token')
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [Order.Status.CANCELLED, Order.Status.CONFIRMED, Order.Status.PAID]
)
def test_cancel_order_fails_when_order_is_not_initiated(client, token, order, status):
    order.user = token.user
    order.status = status
    order.save()
    status, response = post_json(client, f'/api/orders/{order.pk}/cancel/', bearer_token=token.key)
    assert status == 400
    assert response == {'error': 'Orders can only be cancelled when initiated'}


@pytest.mark.django_db
def test_cancel_order_fails_when_unregistered_token(client):
    status, response = post_json(client, '/api/orders/1/cancel/', bearer_token=str(uuid.uuid4()))
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_cancel_order_fails_when_user_is_not_the_owner_of_requested_order(client, token, order):
    status, response = post_json(client, f'/api/orders/{order.pk}/cancel/', bearer_token=token.key)
    assert status == 403
    assert response == {'error': 'User is not the owner of requested order'}


@pytest.mark.django_db
def test_cancel_order_fails_when_order_does_not_exist(client, token):
    status, response = post_json(client, '/api/orders/1/cancel/', bearer_token=token.key)
    assert status == 404
    assert response == {'error': 'Order not found'}


@pytest.mark.django_db
def test_cancel_order_fails_when_method_is_not_allowed(client):
    status, _ = get_json(client, '/api/orders/1/cancel/')
    assert status == 405


# ==============================================================================
# PAY ORDER
# ==============================================================================


@pytest.mark.django_db
def test_pay_order(client, token, order):
    order.user = token.user
    order.status = Order.Status.CONFIRMED
    order.save()
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2099',
        'cvc': '123',
    }
    status, response = post_json(client, f'/api/orders/{order.pk}/pay/', data, token.key)
    assert status == 200
    assert response['status'] == 'Paid'
    assert Order.objects.get(pk=order.pk, status=Order.Status.PAID)


@pytest.mark.django_db
def test_pay_order_fails_when_invalid_json_body(client):
    status, response = post_json(client, '/api/orders/1/pay/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_pay_order_fails_when_invalid_token(client):
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2099',
        'cvc': '123',
    }
    status, response = post_json(client, '/api/orders/1/pay/', data, 'invalid-token')
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
def test_pay_order_fails_when_missing_required_fields(client):
    status, response = post_json(client, '/api/orders/1/pay/')
    assert status == 400
    assert response == {'error': 'Missing required fields'}


@pytest.mark.django_db
def test_pay_order_fails_when_order_is_not_confirmed(client, token, order):
    order.user = token.user
    order.save()
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2099',
        'cvc': '123',
    }
    status, response = post_json(client, f'/api/orders/{order.pk}/pay/', data, token.key)
    assert status == 400
    assert response == {'error': 'Orders can only be paid when confirmed'}


@pytest.mark.django_db
def test_pay_order_fails_when_invalid_card_number(client, token, order):
    order.user = token.user
    order.status = Order.Status.CONFIRMED
    order.save()
    data = {
        'card-number': '1234-1234-1234-123',
        'exp-date': '01/2099',
        'cvc': '123',
    }
    status, response = post_json(client, f'/api/orders/{order.pk}/pay/', data, token.key)
    assert status == 400
    assert response == {'error': 'Invalid card number'}


@pytest.mark.django_db
def test_pay_order_fails_when_invalid_card_expiration_date(client, token, order):
    order.user = token.user
    order.status = Order.Status.CONFIRMED
    order.save()
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/99',
        'cvc': '123',
    }
    status, response = post_json(client, f'/api/orders/{order.pk}/pay/', data, token.key)
    assert status == 400
    assert response == {'error': 'Invalid expiration date'}


@pytest.mark.django_db
def test_pay_order_fails_when_invalid_cvc(client, token, order):
    order.user = token.user
    order.status = Order.Status.CONFIRMED
    order.save()
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2099',
        'cvc': '12',
    }
    status, response = post_json(client, f'/api/orders/{order.pk}/pay/', data, token.key)
    assert status == 400
    assert response == {'error': 'Invalid CVC'}


@pytest.mark.django_db
def test_pay_order_fails_when_card_has_expired(client, token, order):
    order.user = token.user
    order.status = Order.Status.CONFIRMED
    order.save()
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2020',
        'cvc': '123',
    }
    status, response = post_json(client, f'/api/orders/{order.pk}/pay/', data, token.key)
    assert status == 400
    assert response == {'error': 'Card expired'}


@pytest.mark.django_db
def test_pay_order_fails_when_unregistered_token(client):
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2099',
        'cvc': '123',
    }
    status, response = post_json(client, '/api/orders/1/pay/', data, str(uuid.uuid4()))
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_pay_order_fails_when_user_is_not_the_owner_of_requested_order(client, token, order):
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2099',
        'cvc': '123',
    }
    status, response = post_json(client, f'/api/orders/{order.pk}/pay/', data, token.key)
    assert status == 403
    assert response == {'error': 'User is not the owner of requested order'}


@pytest.mark.django_db
def test_pay_order_fails_when_order_does_not_exist(client, token):
    data = {
        'card-number': '1234-1234-1234-1234',
        'exp-date': '01/2099',
        'cvc': '123',
    }
    status, response = post_json(client, '/api/orders/1/pay/', data, token.key)
    assert status == 404
    assert response == {'error': 'Order not found'}


@pytest.mark.django_db
def test_pay_order_fails_when_method_is_not_allowed(client):
    status, _ = get_json(client, '/api/orders/1/pay/')
    assert status == 405
