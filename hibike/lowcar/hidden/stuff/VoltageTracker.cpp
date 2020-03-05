#include "VoltageTracker.h"
#include "pdb_defs.h"

VoltageTracker::VoltageTracker() {
	v_cell1 = 0;  // param 3
	v_cell2 = 0;  // param 4
	v_cell3 = 0;  // param 5
	v_batt = 0;   // param 6
	dv_cell2 = 0; // param 7
	dv_cell3 = 0; // param 8
	vref_guess = 0; // param 9

	triple_calibration = true; //decide whether to use triple calibration or simpler single calibration
}

float VoltageTracker::get_voltage (PARAMS param)
{
	switch (param) {
		case V_CELL1: return v_cell1;
		case V_CELL2: return v_cell2;
		case V_CELL3: return v_cell3;
		case V_BATT: return v_batt;
		case DV_CELL2: return dv_cell2;
		case DV_CELL3: return dv_cell3;
		case VREF_GUESS: return vref_guess;
		default: return 0;
	}
}

void VoltageTracker::set_voltage (PARAMS param, float value)
{

	switch (param) {
		case V_CELL1: v_cell1 = value;
				break;
		case V_CELL2: v_cell2 = value;
				break;
		case V_CELL3: v_cell3 = value;
				break;
		case V_BATT: v_batt = value;
				break;
		case DV_CELL2: dv_cell2 = value;
				break;
		case DV_CELL3: dv_cell3 = value;
				break;
		case VREF_GUESS: vref_guess = value;
				break;
	}
}

float VoltageTracker::get_calib (uint8_t index)
{
	return calib[index];
}

void VoltageTracker::set_calib (uint8_t index, float value)
{
	calib[index] = value;
}

bool VoltageTracker::get_triple_calibration ()
{
	return triple_calibration;
}

void VoltageTracker::set_triple_calibration (bool triple_cal)
{
	triple_calibration = triple_cal;
}
