import re

FILE_READ_ONLY = "r"
NAME_FIELD 			= "name"
QUIZ_FIELD 			= "quiz"
ASSIGNMENT_FIELD 	= "assignment"
MIDTERM_FIELD 		= "midterm"
FINAL_FIELD 		= "final"

# Get the contents of a file by filename
def get_file(filename):
	file_obj = open(filename, FILE_READ_ONLY)
	file_lines = file_obj.readlines()
	file_string = ""
	
	for line in file_lines:
		file_string += line
	
	return file_string

# Parse a file into a list of grade data-sets for students
def parse_file(file_contents):
	# Constants
	GRADE_FORMAT = r"\w+,(\s*\d+\s*,){11}(\s*\d+\s*)"
	LABEL_FIELD = "label"
	LOCATION_FIELD = "location"
	VALUES_TO_DROP_FIELD = "num_drop"
	
	"""
	Grade field name and location table
		------------------------------------------------------------------------------------------------------------
		|              FIELD NAME              |  LOCATION IN RAW GRADE STRING  |   NUMBER OF LOW SCORES TO DROP   |
		------------------------------------------------------------------------------------------------------------
	"""
	GRADE_FIELD_TABLE = [
	
		{ LABEL_FIELD: 		NAME_FIELD, 		LOCATION_FIELD: [0], 				VALUES_TO_DROP_FIELD : 0	},
		{ LABEL_FIELD: 		QUIZ_FIELD, 		LOCATION_FIELD: [1, 2, 3, 4, 5, 6], VALUES_TO_DROP_FIELD : 2	},
		{ LABEL_FIELD: 		ASSIGNMENT_FIELD, 	LOCATION_FIELD: [7, 8, 9, 10], 		VALUES_TO_DROP_FIELD : 1	},
		{ LABEL_FIELD: 		MIDTERM_FIELD, 		LOCATION_FIELD: [11], 				VALUES_TO_DROP_FIELD : 0	},
		{ LABEL_FIELD: 		FINAL_FIELD, 		LOCATION_FIELD: [12], 				VALUES_TO_DROP_FIELD : 0	}
		
	]
	
	# Variables
	grade_format_pattern = re.compile(GRADE_FORMAT)
	matches = grade_format_pattern.finditer(file_contents)
	parsed_grades = list()
	
	for match in matches:
		# For those substrings that are of valid grade format, separate them by comma into a list of values
		grade_str = file_contents[ match.start() : match.end() ]
		grade_components = grade_str.split(',')
		grade_obj = dict()
		
		for field in GRADE_FIELD_TABLE:
			field_value = ""
			
			# Get the values from the grade components by their specified location(s)
			value_list = [ grade_components[i].strip() for i in field[LOCATION_FIELD] ]
			
			# If there's more than one value, we can assume they're numeric due to the regular expression. Drop lowest values and set the average of these values
			if len(value_list) == 1:
				field_value = value_list[0]
			elif len(value_list) > 1:
				num_value_list = [ float(value) for value in value_list ]
				
				# Drop the lowest values
				num_value_list.sort(reverse=True)
				num_value_list_wo_lowest = [ num_value_list[i] for i in range(len(num_value_list) - field[VALUES_TO_DROP_FIELD]) ]
				
				# Get the average
				field_value = get_average_value(num_value_list_wo_lowest)
				
			grade_obj.update( { field[LABEL_FIELD] : field_value } )
		
		parsed_grades.append(grade_obj)
	
	# Warning message for invalid format
	print("%d students were processed. If this is fewer than the number of students inputted, please check your formatting!" % len(parsed_grades))
	
	return parsed_grades

# Find the mean of a set of numbers
def get_average_value(list_values):
	return sum(list_values) / len(list_values)

# Create an object containing each student and a note of pass or fail based off of their grade data
def determine_students_pass_fail(grade_data_list):
	# Constants
	PASS_STRING = "pass"
	FAIL_STRING = "fail"
	BEST_SCORE = 100.0
	SCORE_TO_PASS = 60.0
	SCORE_WEIGHTS = {
		QUIZ_FIELD : 25.0,
		ASSIGNMENT_FIELD : 25.0,
		MIDTERM_FIELD : 25.0,
		FINAL_FIELD : 25.0
	}

	# Variables
	pass_fail_obj = dict()
	
	# For each student, aggregate each sub-score and weigh them by their determined weight
	# If the total score is the required to pass, pass the student, otherwise fail the student
	for grade_data in grade_data_list:
		student_score = sum( [ (float(grade_data[field]) / BEST_SCORE) * SCORE_WEIGHTS[field] for field in SCORE_WEIGHTS ] )
		student_pass_fail = FAIL_STRING if student_score < SCORE_TO_PASS else PASS_STRING
		pass_fail_obj.update( { grade_data[NAME_FIELD] : student_pass_fail } )
	
	return pass_fail_obj

# Driver function
def grade_calculation(filename):
    file_contents = get_file(filename)
    parsed_file = parse_file(file_contents)
    students_pass_fail = determine_students_pass_fail(parsed_file)
    return students_pass_fail