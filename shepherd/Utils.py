# pylint: disable=invalid-name
class SHEPHERD_HEADER():
    START_NEXT_STAGE = "start_next_stage"
        # START_NEXT_STAGE{}: starts the next stage

    RESET_CURRENT_STAGE = "reset_current_stage"
        # RESET_CURRENT_STAGE{}: resets the current stage

    RESET_MATCH = "reset_match"
        # RESET_MATCH{}: resets the current match

    GET_MATCH_INFO = "get_match_info"
        # GET_MATCH_INFO{match_number}: gets match info for given match number

    SETUP_MATCH = "setup_match"
        # SETUP_MATCH{b1name, b1#, b2name, b2#, g1name, g1#, g2name, g2#, match#}:
        # sets up the match given the corresponding info about the teams and match number
        # also has {g1_custom_ip, g2_custom_ip, b1_custom_ip, b2_custom_ip}

    GET_CONNECTION_STATUS = "get_connection_status"
        # GET_CONNECTION_STATUS{}: requested from the Staff UI to check robot
        # connection statuses

    GET_SCORES = "get_scores"
        # GET_SCORES{}: gets scores of the match

    SCORE_ADJUST = "score_adjust"
        # SCORE_ADJUST{blue_score, gold_score}: adjusts the current scores to the input scores

    STAGE_TIMER_END = "stage_timer_end"
        # STAGE_TIMER_END{}: ends the stage's timer

    ROBOT_OFF = "robot_off"
        # ROBOT_OFF{team_number}: takes in team number and disables their robot

    END_EXTENDED_TELEOP = "end_extended_teleop"
        # END_EXTENDED_TELEOP{}: ends the extended teloperated period

    CODE_RETRIEVAL = "code_retrieval"
        # CODE_RETRIEVAL{alliance, result}: retrieves code (from sensors.py)

    CODE_APPLICATION = "code_application"
        # CODE_APPLICATION{alliance, result}: applies code (from sensors.py)

    MASTER_ROBOT = "master_robot"

    FINAL_SCORE = "final_score"
    ASSIGN_TEAMS = "assign_teams"
        # ASSIGN_TEAMS{g1num, g2num, b1num, b2num}
    TEAM_RETRIEVAL = "team_retrieval"
        # TEAM_RETRIEVAL{}

    ROBOT_CONNECTION_STATUS = "robot_connection_status"
        #ROBOT_CONNECTION_STATUS{team_number, connection[True/False]}

    REQUEST_CONNECTIONS = "request_connections"
        #REQUEST_CONNECTIONS{}

# pylint: disable=invalid-name
class DAWN_HEADER():
    CODES = "codes"
    DECODE = "decode"
    SPECIFIC_ROBOT_STATE = "srt"
    MASTER = "master"
    IP_ADDRESS = "ip_address"
    ROBOT_STATE = "rs"
    HEARTBEAT = "heartbeat"
    RESET = "reset"
    #TODO this^

class RUNTIME_HEADER():
    SPECIFIC_ROBOT_STATE = "specific_robot_state"
        # SPECIFIC_ROBOT_STATE{team_number, autonomous, enabled}
        # robot ip is 192.168.128.teamnumber
    DECODE = "decode"
        # DECODE{team_number, seed}

# pylint: disable=invalid-name
class UI_HEADER():
    TEAMS_INFO = "teams_info"
    SCORES = "scores"
    CONNECTIONS = "connections"
    #CONNECTIONS{g_1_connection[True/False], g_2_connection[True/False],
    # b_1_connection[True/False], b_2_connection[True/False]}

# pylint: disable=invalid-name
class SCOREBOARD_HEADER():
    SCORE = "score"
    TEAMS = "teams"
    STAGE = "stage"
    STAGE_TIMER_START = "stage_timer_start"
    RESET_TIMERS = "reset_timers"
    ALL_INFO = "all_info"

class TABLET_HEADER():
    TEAMS = "teams"
    #{b1num, b2num, g1num, g2num}
    CODE = "code"
    #{alliance, code}
    COLLECT_CODES = "collect_codes"
    #{}
    RESET = "reset"
    #{}

# pylint: disable=invalid-name
class CONSTANTS():
    AUTO_TIME = 30 # 30
    TELEOP_TIME = 180 # 180
    SPREADSHEET_ID = "1vurNOrlIIeCHEtK5aJVDfHrRM1AC2qWvIbtWqUgnmLk"
    CSV_FILE_NAME = "Sheets/fc2019.csv"
    STUDENT_DECODE_TIME = 1

# pylint: disable=invalid-name
class ALLIANCE_COLOR():
    GOLD = "gold"
    BLUE = "blue"

# pylint: disable=invalid-name
class LCM_TARGETS():
    SHEPHERD = "lcm_target_shepherd"
    SCOREBOARD = "lcm_target_scoreboard"
    SENSORS = "lcm_target_sensors"
    UI = "lcm_target_ui"
    DAWN = "lcm_target_dawn"
    RUNTIME = "lcm_target_runtime"
    TABLET = "tablet"

# pylint: disable=invalid-name
class TIMER_TYPES():
    MATCH = {"TYPE":"match", "NEEDS_FUNCTION": True,
             "FUNCTION":SHEPHERD_HEADER.STAGE_TIMER_END}
    STUDENT_DECODE = {"TYPE":"student_decode", "NEEDS_FUNCTION": True,
                      "FUNCTION":SHEPHERD_HEADER.CODE_RETRIEVAL}

# pylint: disable=invalid-name
class STATE():
    SETUP = "setup"
    AUTO = "auto"
    WAIT = "wait"
    TELEOP = "teleop"
    END = "end"
