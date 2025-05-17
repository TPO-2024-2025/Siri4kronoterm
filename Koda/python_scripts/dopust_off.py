# Constants from configuration
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
HOLIDAY_DAYS_REGISTER = 2138  # Holiday duration register
HOLIDAY_MODE_REGISTER = 2021  # Holiday mode on/off register
POWER_STATUS_REGISTER = 2011  # Heat pump power status register
HOLIDAY_DAYS = 0  # Number of days for holiday mode

try:
    # Log the start of the script
    logger.info("Starting heat pump holiday mode setup")
    
    # First check if heat pump is on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")
    
    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Holiday Script Error',
            'message': error_msg,
            'notification_id': 'heat_pump_holiday_notification'
        })
    elif heat_pump_state.state == '0':  # Heat pump is off
        message = "Heat pump is currently turned off. Cannot set holiday mode."
        logger.warning(message)
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'notification_id': 'heat_pump_holiday_notification'
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
        # Heat pump is on, proceed with setting holiday mode
        logger.info(f"Setting holiday mode for {HOLIDAY_DAYS} days")
        
        # Step 1: Set the number of holiday days
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': HOLIDAY_DAYS_REGISTER,
            'value': HOLIDAY_DAYS
        })
        
        logger.info(f"Holiday days set to: {HOLIDAY_DAYS}")
        
        # Step 2: Activate holiday mode
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': HOLIDAY_MODE_REGISTER,
            'value': 0  # 0 = OFF
        })
        
        logger.info("Holiday mode deactivated")
        
        # Prepare notification message
        message = f"Heat pump holiday mode deactivated"
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Holiday Mode',
            'message': message,
            'notification_id': 'heat_pump_holiday_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Heat Pump Holiday Mode',
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
    error_msg = f"Error in heat pump holiday script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Heat Pump Holiday Script Error',
        'message': error_msg,
        'notification_id': 'heat_pump_holiday_notification'
    })
    
    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Heat Pump Holiday Script Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })