/**
 * Haxors
 */

import React from 'react';
import _ from 'lodash';
import { Panel, Accordion, ListGroup } from 'react-bootstrap';
import { PeripheralTypes } from '../constants/Constants';
import Peripheral from './Peripheral';

const cleanerNames = {};
cleanerNames[PeripheralTypes.MOTOR_SCALAR] = 'Motors';
cleanerNames[PeripheralTypes.SENSOR_BOOLEAN] = 'Boolean Sensors';
cleanerNames[PeripheralTypes.SENSOR_SCALAR] = 'Numerical Sensors';
cleanerNames[PeripheralTypes.LimitSwitch] = 'Limit Switches';
cleanerNames[PeripheralTypes.LineFollower] = 'Line Followers';
cleanerNames[PeripheralTypes.Potentiometer] = 'Potentiometers';
cleanerNames[PeripheralTypes.Encoder] = 'Encoders';
cleanerNames[PeripheralTypes.ColorSensor] = 'Color Sensors';
cleanerNames[PeripheralTypes.MetalDetector] = 'Metal Detectors';
cleanerNames[PeripheralTypes.ServoControl] = 'Servo Controllers';


const handleAccordion = (array) => {
  const peripheralGroups = {};
  array.forEach((p) => {
    if (!(p.device_type in peripheralGroups)) {
      peripheralGroups[p.device_type] = [];
    }
    peripheralGroups[p.device_type].push(p);
  });
  return (
      _.map(Object.keys(peripheralGroups), groups => (
        <Accordion style={{ marginBottom: '2px' }} key={`${cleanerNames[groups]}-Accordion`}>
          <Panel header={cleanerNames[groups]} key={`${cleanerNames[groups]}-Panel`}>
            {
              _.map(peripheralGroups[groups], peripheral => (
                <Peripheral
                  key={String(peripheral.uid.high) + String(peripheral.uid.low)}
                  id={String(peripheral.uid.high) + String(peripheral.uid.low)}
                  name={peripheral.device_name}
                  value={peripheral.value}
                  peripheralType={peripheral.device_type}
                />
              ))
            }
          </Panel>
        </Accordion>
      ))
  );
};


const FinalCompPeripheralList = (props) => {
  let errorMsg = null;
  if (!props.connectionStatus) {
    errorMsg = 'You are currently disconnected from the robot.';
  } else if (!props.runtimeStatus) {
    errorMsg = 'There appears to be some sort of Runtime error. ' +
      'No data is being received.';
  }

  return (
    <Panel
      id="peripherals-panel"
      header="Peripherals"
      bsStyle="primary"
    >
      <ListGroup fill style={{ marginBottom: '5px' }}>
        {
          !errorMsg ? handleAccordion(
            _.sortBy(_.toArray(props.peripherals), ['device_type', 'device_name']))
          : <p className="panelText">{errorMsg}</p>
        }
      </ListGroup>
    </Panel>
  );
};

FinalCompPeripheralList.propTypes = {
  connectionStatus: React.PropTypes.bool,
  runtimeStatus: React.PropTypes.bool,
  peripherals: React.PropTypes.object,
};

export default FinalCompPeripheralList;
