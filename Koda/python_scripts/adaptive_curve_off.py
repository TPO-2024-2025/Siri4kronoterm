# Constants for adaptive curve setup
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
ADAPTIVE_CURVE_REGISTER = 2320  # Adaptive curve register
POWER_STATUS_REGISTER = 2011    # Heat pump power status sensor

try:
    # Log the start of the script
    logger.info("Starting heat pump adaptive curve setup")
    
    # First check if heat pump is on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")
    
    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Adaptive Curve Script Error',
            'message': error_msg,
            'notification_id': 'heat_pump_adaptive_curve_notification'
        })
    elif heat_pump_state.state == '0':  # Heat pump is off
        message = "Heat pump is currently turned off. Cannot activate adaptive curve."
        logger.warning(message)
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'notification_id': 'heat_pump_adaptive_curve_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'data': {
                'channel': 'heat_pump_channel',
                'importance': 'high',
                'ttl': 0,
                'priority': 'high',
                'vibrationPattern': '100, 100, 100'
            }
        })
    else:
        # Heat pump is on, proceed with activating adaptive curve
        logger.info("Activating heat pump adaptive curve")
        
        # Write to adaptive curve register
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': ADAPTIVE_CURVE_REGISTER,
            'value': 0  # 0 = OFF
        })
        
        logger.info("Adaptive curve deactivated")
        
        # Prepare notification message
        message = "Heat pump adaptive curve has been deactivated"
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Adaptive Curve',
            'message': message,
            'notification_id': 'heat_pump_adaptive_curve_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Heat Pump Adaptive Curve',
            'message': message,
            'data': {
                'channel': 'heat_pump_channel',
                'importance': 'high',
                'ttl': 0,
                'priority': 'high',
                'vibrationPattern': '100, 100, 100'
            }
        })
            
except Exception as e:
    # Log any errors
    error_msg = f"Error in heat pump adaptive curve script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Heat Pump Adaptive Curve Script Error',
        'message': error_msg,
        'notification_id': 'heat_pump_adaptive_curve_notification'
    })
    
    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Heat Pump Adaptive Curve Script Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })
