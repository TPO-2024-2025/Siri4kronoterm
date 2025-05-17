# Constants for heat pump setup
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
POWER_STATUS_REGISTER = 2011    # Heat pump power status register

try:
    # Log the start of the script
    logger.info("Starting heat pump activation")
    
    # First check if heat pump is already on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")
    
    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Activation Error',
            'message': error_msg,
            'notification_id': 'heat_pump_activation_notification'
        })
    elif heat_pump_state.state == '1':  # Heat pump is already on
        message = "Heat pump is already turned on. No action needed."
        logger.info(message)
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Already Running',
            'message': message,
            'notification_id': 'heat_pump_activation_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Heat Pump Already Running',
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
        # Heat pump is off, proceed with activation
        logger.info("Turning on heat pump")
        
        # Write to power status register
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': POWER_STATUS_REGISTER,
            'value': 1  # 1 = ON
        })
        
        logger.info("Heat pump activated")
        
        # Prepare notification message
        message = "Heat pump has been turned on"
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Activation',
            'message': message,
            'notification_id': 'heat_pump_activation_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Heat Pump Activation',
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
    error_msg = f"Error in heat pump activation script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Heat Pump Activation Error',
        'message': error_msg,
        'notification_id': 'heat_pump_activation_notification'
    })
    
    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Heat Pump Activation Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })