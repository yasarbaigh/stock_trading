

def should_place_order(script_name, orders, positions):
    pass
    if orders.get('data') is not None:
        for item in orders.get('data', []):
            if item.get('tradingsymbol') == script_name and item.get('orderstatus') in ['pending', 'completed',
                                                                                        'cancelled', 'rejected']:
                return False
    return True
