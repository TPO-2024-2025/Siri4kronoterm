# Constants for sanitary water setup
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
SANITARY_WATER_REGISTER = 2025  # Sanitary water register
POWER_STATUS_REGISTER = 2011    # Heat pump power status sensor

try:
    # Log the start of the script
    logger.info("Starting sanitary water deactivation")
    
    # First check if heat pump is on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")
    
    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Sanitary Water Deactivation Error',
            'message': error_msg,
            'notification_id': 'sanitary_water_deactivation_notification'
        })
    elif heat_pump_state.state == '0':  # Heat pump is off
        message = "Heat pump is currently turned off. Cannot deactivate sanitary water."
        logger.warning(message)
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'notification_id': 'sanitary_water_deactivation_notification'
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
        # Heat pump is on, proceed with deactivating sanitary water
        logger.info("Deactivating sanitary water")
        
        # Write to sanitary water register
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': SANITARY_WATER_REGISTER,
            'value': 0  # 0 = OFF
        })
        
        logger.info("Sanitary water deactivated")
        
        # Prepare notification message
        message = "Sanitary water has been deactivated"
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Sanitary Water Deactivation',
            'message': message,
            'notification_id': 'sanitary_water_deactivation_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Sanitary Water Deactivation',
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
    error_msg = f"Error in sanitary water deactivation script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Sanitary Water Deactivation Error',
        'message': error_msg,
        'notification_id': 'sanitary_water_deactivation_notification'
    })
    
    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Sanitary Water Deactivation Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })