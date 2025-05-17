# Constants from your configuration
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
TEMPERATURE_REGISTER = 2048  # Želena temperatura register
POWER_STATUS_REGISTER = 2011  # Vklop/izklop črpalke register
TEMP_INCREMENT = 1.0
DEFAULT_TEMP = 22.0  # Default temperature if sensor is unavailable
MAX_TEMPERATURE = 27.0  # Maximum allowed temperature

try:
    # Log the start of the script
    logger.info("Starting heat pump temperature increment")
    
    # First check if heat pump is on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")
    
    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Script Error',
            'message': error_msg,
            'notification_id': 'heat_pump_notification'
        })
    elif heat_pump_state.state == '0':  # Heat pump is off
        message = "Heat pump is currently turned off. Cannot adjust temperature."
        logger.warning(message)
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'notification_id': 'heat_pump_notification'
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
        # Heat pump is on, proceed with temperature adjustment
        # Get current temperature from entity state
        entity_id = "sensor.sanitarna_voda_temperature_okrog_2"
        
        # Get the current state of the temperature sensor
        current_state = hass.states.get(entity_id)
        
        if current_state is None:
            error_msg = f"Could not find entity {entity_id}"
            logger.error(error_msg)
            hass.services.call('persistent_notification', 'create', {
                'title': 'Heat Pump Script Error',
                'message': error_msg,
                'notification_id': 'heat_pump_notification'
            })
        else:
            # Get current temperature value
            if current_state.state in ('unavailable', 'unknown', 'none', ''):
                logger.warning(f"Sensor {entity_id} is {current_state.state}, using default temperature of {DEFAULT_TEMP}°C")
                current_temp = DEFAULT_TEMP
                is_default = True
            else:
                try:
                    current_temp = float(current_state.state)
                    is_default = False
                    logger.info(f"Current temperature setting: {current_temp}°C")
                except ValueError:
                    logger.warning(f"Invalid temperature value in entity state: {current_state.state}, using default of {DEFAULT_TEMP}°C")
                    current_temp = DEFAULT_TEMP
                    is_default = True
            
            # Calculate new temperature
            new_temp = current_temp + TEMP_INCREMENT
            
            # Check if new temperature would exceed maximum
            if new_temp > MAX_TEMPERATURE:
                logger.warning(f"New temperature {new_temp}°C would exceed maximum of {MAX_TEMPERATURE}°C. Limiting to maximum.")
                new_temp = MAX_TEMPERATURE
                message = f"Heat pump temperature limited to maximum {MAX_TEMPERATURE}°C (from {current_temp}°C)"
            else:
                # Normal temperature increase message
                if is_default:
                    message = f"Heat pump temperature set to {new_temp}°C (increased from default of {current_temp}°C because sensor was {current_state.state})"
                else:
                    message = f"Heat pump temperature increased from {current_temp}°C to {new_temp}°C"
            
            # Convert to raw value (multiplied by 10)
            new_temp_raw = int(new_temp * 10)
            
            # Use modbus.write_register service to update the temperature
            hass.services.call('modbus', 'write_register', {
                'hub': MODBUS_HUB,
                'unit': MODBUS_SLAVE,
                'address': TEMPERATURE_REGISTER,
                'value': new_temp_raw
            })
            
            logger.info(message)
            
            # Create persistent notification in Home Assistant UI
            hass.services.call('persistent_notification', 'create', {
                'title': 'Heat Pump Update',
                'message': message,
                'notification_id': 'heat_pump_notification'
            })
            
            # Send notification to mobile device via companion app
            hass.services.call('notify', 'mobile_app', {
                'title': 'Heat Pump Update',
                'message': message,
                'data': {
                    'channel': 'heat_pump_channel',  # Custom notification channel
                    'importance': 'high',           # Make notification important
                    'ttl': 0,                       # Time to live (0 = persistent until clicked)
                    'priority': 'high',             # High priority notification
                    'vibrationPattern': '100, 100, 100'  # Short vibration pattern
                }
            })
            
except Exception as e:
    # Log any errors
    error_msg = f"Error in heat pump script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Heat Pump Script Error',
        'message': error_msg,
        'notification_id': 'heat_pump_notification'
    })
    
    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Heat Pump Script Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })