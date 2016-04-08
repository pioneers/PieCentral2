import React from 'react';
import AceEditor from 'react-ace';
import brace from 'brace';
import EditorActionCreators from '../actions/EditorActionCreators';
import EditorStore from '../stores/EditorStore';
import AlertActions from '../actions/AlertActions';
import EditorToolbar from './EditorToolbar';
import Mousetrap from 'mousetrap';
import smalltalk from 'smalltalk';
import _ from 'lodash';
import ConsoleOutput from './ConsoleOutput';
import RobotActions from '../actions/RobotActions';
import Ansible from '../utils/Ansible';
import {Panel} from 'react-bootstrap';
import { EditorButton } from './EditorClasses';
import ace from 'brace';
import 'brace/ext/language_tools';
import 'brace/ext/searchbox';
import 'brace/mode/python';
// React-ace themes
import 'brace/theme/monokai';
import 'brace/theme/github';
import 'brace/theme/tomorrow';
import 'brace/theme/kuroir';
import 'brace/theme/twilight';
import 'brace/theme/xcode';
import 'brace/theme/textmate';
import 'brace/theme/solarized_dark';
import 'brace/theme/solarized_light';
import 'brace/theme/terminal';
import {remote} from 'electron';
let langtools = ace.acequire('ace/ext/language_tools');
let storage = remote.require('electron-json-storage');

export default React.createClass({
  getInitialState() {
    return {
      showConsole: false,
      filepath: null,
      latestSaveCode: '',
      editorCode: '',
      editorTheme: 'github',
      gameEnable: false,
      gameAuto: false,
      fontSize: 14
    };
  },
  componentDidMount() {
    this.refs.CodeEditor.editor.setOption('enableBasicAutocompletion', true);

    Mousetrap.prototype.stopCallback = function(e, element, combo) {
      return false; // Always respond to keyboard combos
    };

    Mousetrap.bind(['mod+s'], (e)=>{
      if (e.preventDefault) {
        e.preventDefault();
      }
      this.saveFile();
    });

    // If possible, reopen the last opened file.
    let lastFile = localStorage.getItem('lastFile');
    if (lastFile !== null) {
      EditorActionCreators.readFilepath(lastFile);
    }

    storage.has('editorTheme').then((hasKey)=>{
      if (hasKey) {
        storage.get('editorTheme').then((data)=>{
          this.setState({
            editorTheme: data.theme
          });
        });
      } else {
        storage.set('editorTheme', {
          theme: 'github'
        }, (err)=>{
          if (err) throw err;
        });
      }
    });

    EditorStore.on('change', this.updateEditorData);
  },
  componentWillUnmount() {
    Mousetrap.unbind(['mod+s']);
    EditorStore.removeListener('change', this.updateEditorData);
  },
  updateEditorData() {
    this.setState({
      filepath: EditorStore.getFilepath(),
      latestSaveCode: EditorStore.getLatestSaveCode(),
      editorCode: EditorStore.getEditorCode()
    });
  },
  openFile() {
    if (this.hasUnsavedChanges()) {
      smalltalk.confirm(
        'Are you sure?',
        'You have unsaved changes, opening a new file will discard them!'
      ).then(()=>{
        EditorActionCreators.openFile();
      }, ()=>{
        console.log('Canceled');
      });
    } else {
      EditorActionCreators.openFile();
    }
  },
  saveFile() {
    EditorActionCreators.saveFile(this.state.filepath, this.state.editorCode);
  },
  saveAsFile() {
    EditorActionCreators.saveFile(null, this.state.editorCode);
  },
  createNewFile() {
    if (this.hasUnsavedChanges()) {
      smalltalk.confirm(
        'Are you sure?',
        'You have unsaved changes, creating a new file will discard them!'
      ).then(()=>{
        EditorActionCreators.createNewFile();
      }, ()=>{
        console.log('Canceled');
      });
    } else {
      EditorActionCreators.createNewFile();
    }
  },
  editorUpdate(newVal) {
    EditorActionCreators.editorUpdate(newVal);
  },
  correctText(text) {
    // Removes non-ASCII characters from text.
    return text.replace(/[^\x00-\x7F]/g, "");
  },
  onEditorPaste(pasteData) {
    // Must correct non-ASCII characters, which would crash Runtime.
    let correctedText = pasteData.text;
    // Normalizing will allow us (in some cases) to preserve ASCII equivalents.
    correctedText = correctedText.normalize("NFD");
    // Special case to replace fancy quotes.
    correctedText = correctedText.replace(/[”“]/g,'"');
    correctedText = correctedText.replace(/[‘’]/g,"'");
    correctedText = this.correctText(correctedText);
    // TODO: Create some notification that an attempt was made at correcting non-ASCII chars.
    pasteData.text = correctedText;
  },
  toggleConsole() {
    this.setState({showConsole: !this.state.showConsole});
    // must call resize method after changing height of ace editor
    setTimeout(()=>this.refs.CodeEditor.editor.resize(), 0.1);
  },
  clearConsole() {
    RobotActions.clearConsole();
  },
  sendCode(command) {
    let correctedText = this.correctText(this.state.editorCode);
    if (correctedText !== this.state.editorCode) {
      AlertActions.addAlert(
	'Invalid characters detected',
	'Your code has non-ASCII characters, which won\'t work on the robot. ' +
	'Please remove them and try again.'
      );
      return false;
    } else {
      Ansible.sendMessage(command, {
	code: this.state.editorCode
      });
      return true;
    }
  },
  upload() { this.sendCode('upload'); },
  startRobot() {
    let sent = this.sendCode('execute');
    if (sent) {
      RobotActions.clearConsole();
    };
  },
  stopRobot() {
    Ansible.sendMessage('stop', {});
  },
  gameEnable() {
    this.state.gameEnable = !this.state.gameEnable;
    Ansible.sendMessage('game', {enabled: this.state.gameEnable, autonomous: this.state.gameAuto});
  },
  gameAuto() {
    this.state.gameAuto = !this.state.gameAuto;
    Ansible.sendMessage('game', {enabled: this.state.gameEnable, autonomous: this.state.gameAuto});
  },
  openAPI() {
    window.open("https://pie-api.readthedocs.org/")
  },
  fontIncrease() {
    if (this.state.fontSize <= 28) {
      this.state.fontSize += 7;
    }
  },
  fontDecrease() {
    if (this.state.fontSize > 7) {
      this.state.fontSize -= 7;
    }
  },
  generateButtons() {
    // The buttons which will be in the button toolbar
    return [
      {
        groupId: 'file-operations-buttons',
        buttons: [
          new EditorButton('create', 'New', this.createNewFile, 'file'),
          new EditorButton('open', 'Open', this.openFile, 'folder-open'),
          new EditorButton('save', 'Save', this.saveFile, 'floppy-disk'),
          new EditorButton('saveas', 'Save As', this.saveAsFile, 'floppy-save'),
          new EditorButton('api', 'API', this.openAPI, 'book'),
          new EditorButton('zoomin', 'Font Larger', this.fontIncrease, 'zoom-in'),
          new EditorButton('zoomout', 'Font Smaller', this.fontDecrease, 'zoom-out')
        ],
      }, {
        groupId: 'code-execution-buttons',
        buttons: [
          new EditorButton('run', 'Run', this.startRobot, 'play', (this.props.isRunningCode || !this.props.runtimeStatus)),
          new EditorButton('stop', 'Stop', this.stopRobot, 'stop', !(this.props.isRunningCode && this.props.runtimeStatus)),
          new EditorButton('upload', 'Upload', this.upload, 'upload', (this.props.isRunningCode || !this.props.runtimeStatus)),
          new EditorButton('toggle-console', 'Toggle Console', this.toggleConsole, 'console'),
          new EditorButton('clear-console', 'Clear Console', this.clearConsole, 'remove'),
          new EditorButton('enabled', 'Game Enable', this.gameEnable, 'play-circle', false, this.state.gameEnable),
          new EditorButton('autonomous', 'Autonomous', this.gameAuto, 'king', false, this.state.gameAuto)
        ]
      }
    ];
  },
  pathToName(filepath) {
    if (filepath !== null) {
      if (process.platform === 'win32') {
        return filepath.split('\\').pop();
      } else {
        return filepath.split('/').pop();
      }
    } else {
      return '[ New File ]';
    }
  },
  hasUnsavedChanges() {
    return (this.state.latestSaveCode !== this.state.editorCode);
  },
  changeTheme(theme) {
    storage.set('editorTheme', {theme: theme}, (err)=>{
      if (err) throw err;
    });
    this.setState({editorTheme: theme});
  },
  themes: [
    'monokai',
    'github',
    'tomorrow',
    'kuroir',
    'twilight',
    'xcode',
    'textmate',
    'solarized_dark',
    'solarized_light',
    'terminal'
  ],
  render() {
    let consoleHeight = 250;
    let editorHeight = window.innerHeight * 0.66;
    return (
      <Panel
        header={'Editing: ' + this.pathToName(this.state.filepath) +
          (this.hasUnsavedChanges() ? '*' : '')}
        bsStyle="primary">
        <EditorToolbar
          buttons={ this.generateButtons() }
          unsavedChanges={ this.hasUnsavedChanges() }
          changeTheme={ this.changeTheme }
          editorTheme={ this.state.editorTheme }
          themes={ this.themes }
        />
        <AceEditor
          mode="python"
          theme={ this.state.editorTheme }
          width="100%"
          fontSize={this.state.fontSize}
          ref="CodeEditor"
          name="CodeEditor"
          height={String(
            editorHeight - this.state.showConsole * (consoleHeight + 30)) + 'px'}
          value = { this.state.editorCode }
          onChange={ this.editorUpdate }
	  onPaste={ this.onEditorPaste }
          editorProps={{$blockScrolling: Infinity}}
        />
        <ConsoleOutput
          toggleConsole={this.toggleConsole}
          show={this.state.showConsole}
          height={consoleHeight}
          output={this.props.consoleData}/>
      </Panel>
    );
  }
});
