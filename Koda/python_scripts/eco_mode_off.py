# Constants from configuration
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
ECO_MODE_REGISTER = 2012  # ECO mode register
POWER_STATUS_REGISTER = 2011  # Heat pump power status register

try:
    # Log the start of the script
    logger.info("Stopping heat pump ECO mode setup")
    
    # First check if heat pump is on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")
    
    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump ECO Script Error',
            'message': error_msg,
            'notification_id': 'heat_pump_eco_notification'
        })
    elif heat_pump_state.state == '0':  # Heat pump is off
        message = "Heat pump is currently turned off. Cannot set ECO mode."
        logger.warning(message)
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'notification_id': 'heat_pump_eco_notification'
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
        # Heat pump is on, proceed with setting ECO mode
        logger.info("Setting heat pump to ECO mode")
        
        # Set ECO mode
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': ECO_MODE_REGISTER,
            'value': 0  # 0 = OFF
        })
        
        logger.info("ECO mode activated")
        
        # Prepare notification message
        message = "Heat pump ECO mode has been deactivated"
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump ECO Mode',
            'message': message,
            'notification_id': 'heat_pump_eco_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Heat Pump ECO Mode',
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
    error_msg = f"Error in heat pump ECO mode script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Heat Pump ECO Script Error',
        'message': error_msg,
        'notification_id': 'heat_pump_eco_notification'
    })
    
    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Heat Pump ECO Script Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })