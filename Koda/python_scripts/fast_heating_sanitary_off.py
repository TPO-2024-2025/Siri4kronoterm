# Constants for sanitary water fast heating setup
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
SANITARY_WATER_REGISTER = 2025         # Sanitary water register
SANITARY_FAST_HEATING_REGISTER = 2014  # Fast heating register
POWER_STATUS_REGISTER = 2011           # Heat pump power status sensor

try:
    # Log the start of the script
    logger.info("Starting sanitary water fast heating activation")

    # First check if heat pump is on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")

    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Sanitary Water Fast Heating Error',
            'message': error_msg,
            'notification_id': 'sanitary_water_fast_heating_notification'
        })
    elif heat_pump_state.state == '0':  # Heat pump is off
        message = "Heat pump is currently turned off. Cannot activate fast heating of sanitary water."
        logger.warning(message)

        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'notification_id': 'sanitary_water_fast_heating_notification'
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
        # Now check if sanitary water is on
        # Read the current state of sanitary water
        sanitary_water_state = None
        try:
            result = hass.states.get(f"sensor.vklop_izklop_sanitarne_vode")
            if result is not None:
                sanitary_water_state = result.state
        except Exception as e:
            logger.warning(f"Could not get sanitary water status from sensor: {str(e)}")
            # If we can't get from a sensor, we'll try to read the register directly
            
        if sanitary_water_state is None or sanitary_water_state == 'unknown':
            # Notify that we're proceeding but couldn't verify sanitary water status
            logger.warning("Could not determine sanitary water status, proceeding with fast heating anyway")
            
        if sanitary_water_state == '0':  # Sanitary water is off
            message = "Sanitary water is not activated. Activating sanitary water before fast heating."
            logger.info(message)
            
            # Activate sanitary water first
            hass.services.call('modbus', 'write_register', {
                'hub': MODBUS_HUB,
                'unit': MODBUS_SLAVE,
                'address': SANITARY_WATER_REGISTER,
                'value': 1  # 1 = ON
            })
            
            logger.info("Sanitary water activated")
            
        # Heat pump is on, proceed with activating fast heating
        logger.info("Activating sanitary water fast heating")

        # Write to fast heating register
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': SANITARY_FAST_HEATING_REGISTER,
            'value': 0  # 1 = ON
        })

        logger.info("Sanitary water fast heating activated")

        # Prepare notification message
        message = "Fast heating of sanitary water has been deactivated"

        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Sanitary Water Fast Heating',
            'message': message,
            'notification_id': 'sanitary_water_fast_heating_notification'
        })

        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Sanitary Water Fast Heating',
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
    error_msg = f"Error in sanitary water fast heating script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Sanitary Water Fast Heating Error',
        'message': error_msg,
        'notification_id': 'sanitary_water_fast_heating_notification'
    })

    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Sanitary Water Fast Heating Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })