# Constants for backup heat source setup
MODBUS_HUB = "heatpump"
MODBUS_SLAVE = 20
BACKUP_SOURCE_REGISTER = 2017     # Backup heat source register
POWER_STATUS_REGISTER = 2011      # Heat pump power status sensor

try:
    # Log the start of the script
    logger.info("Starting backup heat source deactivation")
    
    # First check if heat pump is on
    heat_pump_state = hass.states.get("sensor.vklop_izklop_crpalke")
    
    if heat_pump_state is None:
        error_msg = "Could not find heat pump power status sensor"
        logger.error(error_msg)
        hass.services.call('persistent_notification', 'create', {
            'title': 'Backup Heat Source Script Error',
            'message': error_msg,
            'notification_id': 'backup_heat_source_notification'
        })
    elif heat_pump_state.state == '0':  # Heat pump is off
        message = "Heat pump is currently turned off. Cannot deactivate backup heat source."
        logger.warning(message)
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Heat Pump Not Running',
            'message': message,
            'notification_id': 'backup_heat_source_notification'
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
        # Heat pump is on, proceed with deactivating backup heat source
        logger.info("Deactivating backup heat source")
        
        # Write to backup heat source register
        hass.services.call('modbus', 'write_register', {
            'hub': MODBUS_HUB,
            'unit': MODBUS_SLAVE,
            'address': BACKUP_SOURCE_REGISTER,
            'value': 0  # 0 = OFF
        })
        
        logger.info("Backup heat source deactivated")
        
        # Prepare notification message
        message = "Backup heat source has been deactivated"
        
        # Create persistent notification in Home Assistant UI
        hass.services.call('persistent_notification', 'create', {
            'title': 'Backup Heat Source Deactivation',
            'message': message,
            'notification_id': 'backup_heat_source_notification'
        })
        
        # Send notification to mobile device via companion app
        hass.services.call('notify', 'mobile_app', {
            'title': 'Backup Heat Source Deactivation',
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
    error_msg = f"Error in backup heat source deactivation script: {str(e)}"
    logger.error(error_msg)
    hass.services.call('persistent_notification', 'create', {
        'title': 'Backup Heat Source Script Error',
        'message': error_msg,
        'notification_id': 'backup_heat_source_notification'
    })
    
    # Send error notification to mobile device
    hass.services.call('notify', 'mobile_app', {
        'title': 'Backup Heat Source Script Error',
        'message': error_msg,
        'data': {
            'channel': 'heat_pump_channel',
            'importance': 'high',
            'ttl': 0,
            'priority': 'high',
            'vibrationPattern': '100, 100, 100'
        }
    })