SYNTHETIC_DATA_GENERATE_METHOD = """

You are going to generate synthetic sample data for a database based on Django model definitions.
1) Make sure values match the expected type for each field. 
2) Make sure that the data are plausible real world values.
3) You are going to return one json object, within this json object each model name is associated with an array of instances.
4) Return only one unified json object made from the model arrays please, NO OTHER TEXT THAN JSON.

{all_formatted_model_definitions}

"""
