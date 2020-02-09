import React from 'react';
import {
  Alignment,
  Button,
  ButtonGroup,
  Colors,
  Icon,
  Menu,
  MenuItem,
  Navbar,
  Popover,
  PopoverInteractionKind,
  Tooltip,
} from '@blueprintjs/core';
import { IconNames } from "@blueprintjs/icons";
import { VERSION } from '../constants/Constants';

import DeviceList from './DeviceList';
import PreferencesMenu from './PreferencesMenu';

import { ipcRenderer } from 'electron';

import RuntimeClient from 'runtime-client';

const ConsoleMenu = () => (
  <Menu>
    <MenuItem text="Open" icon={IconNames.MENU_OPEN} />
    <MenuItem text="Close" icon={IconNames.MENU_CLOSED} />
    <MenuItem text="Copy" icon={IconNames.DUPLICATE}></MenuItem>
    <MenuItem text="Clear" icon={IconNames.CLEAN} />
  </Menu>
);

const DebugMenu = () => (
  <Menu>
    <MenuItem text="Lint" icon={IconNames.CODE} />
    <MenuItem text="Restart Runtime" icon={IconNames.RESET} />
    <MenuItem text="Motor check" icon={IconNames.COG} />
    <MenuItem text="Statistics" icon={IconNames.TIMELINE_LINE_CHART} />
  </Menu>
);

const StatusIndicator = () => (
  <span>Healthy</span>
);

class Toolbar extends React.Component {
  render() {
    return (
      <Navbar>
        <Navbar.Group>
          <Navbar.Heading>
            Dawn v
            { VERSION }
          </Navbar.Heading>
          <Navbar.Divider />
          <ButtonGroup>
            <Button icon={IconNames.UPLOAD}>Upload</Button>
            <Button icon={IconNames.DOWNLOAD}>Download</Button>
          </ButtonGroup>
          <Navbar.Divider />
          <ButtonGroup>
            <Button icon={IconNames.PLAY}>Start</Button>
            <Button icon={IconNames.STOP}>Stop</Button>
            <Button icon={IconNames.FLAME}>Emergency</Button>
          </ButtonGroup>
          <Navbar.Divider />
          <ButtonGroup>
            <Popover
                content={<ConsoleMenu />}
                interactionKind={PopoverInteractionKind.HOVER}
                hoverOpenDelay={0}
                hoverCloseDelay={200}>
              <Button icon={IconNames.CONSOLE}>Console</Button>
            </Popover>
            <Popover
                content={<DebugMenu />}
                interactionKind={PopoverInteractionKind.HOVER}
                hoverOpenDelay={0}
                hoverCloseDelay={200}>
              <Button icon={IconNames.DASHBOARD}>Debug</Button>
            </Popover>
            <PreferencesMenu />
          </ButtonGroup>
        </Navbar.Group>
        <Navbar.Group align={Alignment.RIGHT}>
          <Navbar.Heading>
            <StatusIndicator />
          </Navbar.Heading>
        </Navbar.Group>
      </Navbar>
    );
  }
}

class App extends React.PureComponent {
  render() {
    const className = 'bp3-dark';
    const background = Colors.DARK_GRAY1;

    return (
      <div className={`bg-theme bp3-text-large ${className}`} style={{ background }}>
        <Toolbar />
        <div>
          <div className="editor"></div>
          <DeviceList />
        </div>
      </div>
    );
  }
}

export default App;


/*
import Joyride from 'react-joyride';
import PropTypes from 'prop-types';
import { remote, ipcRenderer } from 'electron';
import { connect } from 'react-redux';
import smalltalk from 'smalltalk';
import Dashboard from './Dashboard';
import DNav from './DNav';
import joyrideSteps from './JoyrideSteps';
import { removeAsyncAlert } from '../actions/AlertActions';
import { updateFieldControl } from '../actions/FieldActions';
import { logging, startLog } from '../utils/utils';

const storage = remote.require('electron-json-storage');

class AppComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      steps: [],
      tourRunning: false,
    };
    this.addSteps = this.addSteps.bind(this);
    this.addTooltip = this.addTooltip.bind(this);
    this.startTour = this.startTour.bind(this);
    this.joyrideCallback = this.joyrideCallback.bind(this);
    this.updateAlert = this.updateAlert.bind(this);
    startLog();
  }

  componentDidMount() {
    this.addSteps(joyrideSteps);
    ipcRenderer.on('start-interactive-tour', () => {
      this.startTour();
    });
    storage.has('firstTime', (hasErr, hasKey) => {
      if (hasErr) {
        logging.log(hasErr);
        return;
      }

      if (!hasKey) {
        this.startTour();
        storage.set('firstTime', { first: true }, (setErr) => {
          if (setErr) logging.log(setErr);
        });
      }
    });
  }

  shouldComponentUpdate(nextProps, nextState) {
    return nextProps !== this.props || nextState !== this.state;
  }

  componentDidUpdate(prevProps) {
    const { asyncAlerts } = this.props;
    if (prevProps.asyncAlerts !== asyncAlerts) {
      const latestAlert = asyncAlerts[asyncAlerts.length - 1];
      this.updateAlert(latestAlert);
    }
  }

  addSteps(steps) {
    if (!Array.isArray(steps)) {
      steps = [steps];
    }
    if (steps.length === 0) {
      return;
    }
    this.setState((currentState) => {
      currentState.steps = currentState.steps.concat(steps);
      return currentState;
    });
  }

  addTooltip(data) {
    this.joyride.addTooltip(data);
  }

  startTour() {
    this.setState({ tourRunning: true });
  }

  joyrideCallback(action) {
    if (action.type === 'finished') {
      this.setState({ tourRunning: false });
      this.joyride.reset(false);
    }
  }

  updateAlert(latestAlert) {
    smalltalk.alert(latestAlert.heading, latestAlert.message).then(() => {
      this.props.onAlertDone(latestAlert.id);
    }, () => {
      this.props.onAlertDone(latestAlert.id);
    });
  }

  render() {
    return (
      <div>
        <DNav
          startTour={this.startTour}
          runtimeStatus={this.props.runtimeStatus}
          masterStatus={this.props.masterStatus}
          connectionStatus={this.props.connectionStatus}
          isRunningCode={this.props.isRunningCode}
        />
        <Joyride
          ref={(c) => { this.joyride = c; }}
          steps={this.state.steps}
          type="continuous"
          showSkipButton
          autoStart
          run={this.state.tourRunning}
          callback={this.joyrideCallback}
          locale={{
            back: 'Previous',
            close: 'Close',
            last: 'End Tour',
            next: 'Next',
            skip: 'Skip Tour',
          }}
        />
        <div style={{ height: '35px', marginBottom: '21px' }} />
        <Dashboard
          addSteps={this.addSteps}
          addTooltip={this.addTooltip}
          connectionStatus={this.props.connectionStatus}
          runtimeStatus={this.props.runtimeStatus}
          isRunningCode={this.props.isRunningCode}
        />
      </div>
    );
  }
}

AppComponent.propTypes = {
  connectionStatus: PropTypes.bool.isRequired,
  runtimeStatus: PropTypes.bool.isRequired,
  masterStatus: PropTypes.bool.isRequired,
  isRunningCode: PropTypes.bool.isRequired,
  asyncAlerts: PropTypes.array.isRequired,
  onAlertDone: PropTypes.func.isRequired,
};

const mapStateToProps = (state) => ({
  connectionStatus: state.info.connectionStatus,
  runtimeStatus: state.info.runtimeStatus,
  masterStatus: state.fieldStore.masterStatus,
  isRunningCode: state.info.isRunningCode,
  asyncAlerts: state.asyncAlerts,
});

const mapDispatchToProps = (dispatch) => ({
  onAlertDone(id) {
    dispatch(removeAsyncAlert(id));
  },
});

const App = connect(mapStateToProps, mapDispatchToProps)(AppComponent);

export default App;
*/
