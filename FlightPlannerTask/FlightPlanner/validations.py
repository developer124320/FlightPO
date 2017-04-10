# -*- coding: UTF-8 -*-
'''
Created on Mar 2, 2015

@author: jin
'''

class Validations:
    A_LONGITUDE_VALUE = "a longitude value"
    A_MAGNETIC_VARIATION_VALUE = "a magnetic variation value"
    A_NUMERIC_VALUE = "a numeric value"
    A_SPEED_VALUE = "a speed value"
    A_VALUE = "a value"
    ACCEPTABLE_BEARINGS_ARE_X_Y = unicode("Acceptable bearings are %.1f° - %.1f°", "utf-8")
    ACCEPTABLE_BEARINGS_ARE_X_Y_AND_X_Y = unicode("Acceptable bearings are %.1f° - %.1f° and %.1f° - %.1f°", "utf-8")
    ACCEPTABLE_MINIMUM_DISTANCE_IS_X = "Acceptable minimum distance is %.1f"
    AN_ALTITUDE_VALUE = "an altitude value"
    AN_ANGLE_GRADIENT_SLOPE_VALUE = "an angle/gradient/slope value"
    AN_INTEGER_VALUE = "an integer value"
    BEARING_X_OUTSIDE_OF_VALID_RANGE = "Bearing (%.1f - %.1f) outside of valid range (%.1f - %.1f)"
    CUSTOM_AC_CATEGORY_NOT_SUPPORTED = "Custom aircraft category not supported"
    DATE_NOT_WITHIN_MAGNETIC_MODEL = "The entered date is NOT within the valid time period of the selected magnetic model"
    GREATER_THAN_0 = "greater than 0"
    GREATER_THAN_OR_EQUAL_TO_0 = "greater than or equal to 0"
    INBOUND_OUTBOUND_TRACK_CANNOT_BE_IDENTICAL = "In-bound and out-bound track cannot be identical"
    INVALID_POSITION = "Invalid position!"
    NO_ALTITUDE_INTERVALS_SPECIFIED = "No altitude intervals specified, please use the Settings button to specify the appropriate intervals"
    NOT_VALID_ALTITUDE_VALUE = "%f is not a valid altitude value"
    NOT_VALID_ANGLE_GRADIENT_SLOPE_VALUE = "%f is not a valid angle/gradient/slope value"
    NOT_VALID_DEGREES_VALUE = "%f is not a valid degrees value"
    NOT_VALID_DISTANCE_VALUE = "%f is not a valid distance value"
    NOT_VALID_DURATION_VALUE = "%f is not a valid duration value"
    NOT_VALID_LATITUDE_VALUE = "%f is not a valid latitude value"
    NOT_VALID_LAYER_NAME = "%sf is not a valid layer name"
    NOT_VALID_LONGITUDE_VALUE = "%f is not a valid longitude value"
    NOT_VALID_MAGNETIC_VARIATION_VALUE = "%f is not a valid magnetic variation value"
    NOT_VALID_NUMERIC_VALUE = "%f is not a valid numeric value"
    NOT_VALID_SPEED_VALUE = "%f is not a valid speed value"
    OTHER_THAN_0 = "other than 0"
    PLEASE_ENTER = "Please enter %f"
    PLEASE_ENTER_VALID_MULTIPLIER = "Please enter a valid multiplier value"
    PLEASE_ENTER_VALID_MULTIPLIER_OR_LEAVE_BLANK = "Please enter a valid multiplier value or leave the field blank"
    PLEASE_ENTER_VALID_RUNWAY_POSITIONS = "Please enter valid runway positions"
    PLEASE_ENTER_VALID_TREES_VALUE = "Please enter a valid trees value"
    PLEASE_ENTER_VALID_TREES_VALUE_OR_LEAVE_BLANK = "Please enter a valid trees value or leave the field blank"
    PLEASE_ENTER_VALID_UPPER_LIMIT = "Please enter a valid upper limit altitude value"
    PLEASE_ENTER_VALID_UPPER_LIMIT_OR_LEAVE_BLANK = "Please enter a valid upper limit altitude value or leave the field blank"
    PLEASE_SELECT_A_FILE = "Please select a file"
    PLEASE_SELECT_A_TEMPLATE  = "Please select a template."
    PLEASE_SELECT_A_VALID_LICENSE_FILE = "Please select a valid license file"
    PLEASE_SELECT_AN_ITEM = "Please select an item from the list"
    PLEASE_SELECT_AT_LEAST_1_COLUMN = "Please select at least 1 column"
    POSITION_INSIDE_TURN = "Position inside turn!"
    REQUIRED = "%f required"
    RNAV_AC_CATEGORY_NOT_SUPPORTED  = "%s aircraft category not supported"
    RNAV_FLIGHT_PHASE_NOT_SUPPORTED = "%s flight phase not supported"
    RNAV_SPECIFICATION_NOT_SUPPORTED = "%s specification not supported"
    RNAV_WPT_TYPE_NOT_SUPPORTED = "%s waypoint type not supported"
    SEGMENT_CANNOT_BE_SHORTER_THAN = "Segment cannot be shorter than %f"
    SEGMENT_TRACK_MUST_BE_BETWEEN = unicode("Segment track (%s -> %s, %.3f°) must be within %.3f° - %.3f°", "utf-8")
    UNIQUE_DESIGNATOR_REQUIRED = "Unique designator required"
    UNIQUE_IDENTIFIER_REQUIRED = "Unique identifier required"
    UPPER_LIMIT_MUST_BE_GREATER_THAN = "The upper limit value must be greater than %f"
    UPPER_LIMIT_MUST_BE_GREATER_THAN_AND_SMALLER_THAN = "The upper limit value must be greater than %f and smaller than %f"
    UPPER_LIMIT_MUST_BE_SMALLER_THAN = "The upper limit value must be smaller than %.1f"
    VALUE_CANNOT_BE_GREATER_THAN = "Value cannot be greater than %.1f"
    VALUE_CANNOT_BE_SMALLER_THAN = "Value cannot be smaller than %.1f"
    VALUE_CANNOT_BE_SMALLER_THAN_OR_GREATER_THAN = "Value cannot be smaller than %f or greater than %f"
    VALUE_MUST_BE_A_VALID_TRACK = "Value must be grater than or equal to -360 and smaller than or equal to 360"
    VALUE_MUST_BE_DIFFERENT_FROM_AND = "Value must be different from %f and %f"
    VALUE_MUST_BE_EQUAL_TO = "Value must be equal to %f"
    VALUE_MUST_BE_GREATER_THAN = "Value must be greater than %.1f"
    VALUE_MUST_BE_WITHIN_0_AND_360_DEGREES = unicode("Value must be within 0 - 360°", "utf-8")
    VALUE_MUST_BE_WITHIN_10_AND_15_NM = "Value must be within 10 - 15 nm"
    VALUE_MUST_BE_WITHIN_X_AND_Y_DEGREES = unicode("Value must be within %.1f - %.1f°", "utf-8")
    VALUE_MUST_BE_WITHIN_X_AND_Y_DEGREES_OR_EQUAL_TO = unicode("Value must be within %.1f - %.1f° or equal to %f° for a closing sector", "utf-8")
    VALUE_NOT_WITHIN_ACCEPTABLE_RANGE = "Value is not within the acceptable range"
    
    @staticmethod
    def valueValidate(txtBox, title):
        try:
            value = float(txtBox.text())
            return True
        except ValueError:
            raise UserWarning ,"%s Value is not correct "%title
        