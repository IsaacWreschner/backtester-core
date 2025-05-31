def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

#def get_financial_data(instrument, period, interval='1d'):
#    ticker = yf.Ticker(instrument)
#    data = ticker.history(period=period, interval=interval) 
#    return data
#
#
#def random_buy(data, probabilities):
#    data['random'] = np.random.choice([0, 1], size=len(data), p=probabilities)
#    data['Buy or Sell'] = np.where(
#        data['random'] == 1, 
#       'Buy', 
#       'Sell' 
#    )
#    data['Is positive gain'] = np.where(
#        data['Buy or Sell'] == 'Buy', 
#        (data['Close'] - data['Open'] > 0), 
#        (data['Close'] - data['Open'] < 0)  
#    )
#    return data
#
#def add_margin(data, pips_threshold):
#   data['pips gained'] = np.where(
#        data['random'] == 1, 
#        data['Close'] - data['Open'],   # If random is 1, pips gained is Close - Open
#        data['Open'] - data['Close']    # If random is 0, pips gained is Open - Close
#    )
#   
#   y = 1
#   y_values = []
#   cumulative_pips = 0
#   
#   for pips in data['pips gained']:
#        y_values.append(y)
#        real_pips = pips * y
#        cumulative_pips += real_pips
#        if cumulative_pips > 0:
#          cumulative_pips = 0
#          y = 1
#        else:
#          y = max(abs(cumulative_pips) / pips_threshold, 1.0)
#
#        # Append current value of y
#        
#
#    # Add y values as a new column to the dataframe
#   data['margin'] = y_values
#   data['real gain'] = (data['pips gained'] * data['margin'])
#
#   return data
#
#additional
#
#def my_strategy(session:Session):
#    curr_position = 0
#    for tick in session.get_testing_data().as_single_ticks():
#        if curr_position > 0:
#            # Close the current position
#            session.close_position(
#                id=curr_position,
#                closed_at=tick['datetime'],
#                close_price=tick['price']
#            )
#        curr_position = session.add_position(
#            position_type='sell',
#            start_at=tick['datetime'],
#            price=tick['price']
#        )  
#
#session = tester.start_testing_session(
#    symbol='AAPL',
#    timeframe='1d',
#    start_datetime='2022-01-01',
#    end_datetime='2023-01-01',
#    margin=0.5
#)
#
##print(market_data.as_single_ticks())
#curr_position = 0
#
#
#for tick in session.get_testing_data().as_single_ticks():
#    if curr_position > 0:
#        # Close the current position
#        session.close_position(
#            id=curr_position,
#            closed_at=tick['datetime'],
#            close_price=tick['price']
#        )
#    curr_position = session.add_position(
#        position_type='sell',
#        start_at=tick['datetime'],
#        price=tick['price']
#    )  
#
#print(session.get_all_positions_as_list())
#print(session.get_stats())
#print(session.get_chart_data())  

#from datetime import datetime, timedelta
#from typing import Optional
#from models.parameters import Parameters, ParametersWithoutCustom  # Adjust import as needed
#
#def validate_disabled_user_parameters(parameters: ParametersWithoutCustom, disabled_user_parameters: dict) -> None:
#    """Validate that all disabled parameters are provided."""
#    for parameter_name, is_disabled in disabled_user_parameters.items():
#        if is_disabled:
#            if parameters is None or getattr(parameters, parameter_name, None) is None:
#                raise ValueError(
#                    f"{parameter_name} is disabled for user selection but not provided in parameters."
#                )
#
#def merge_non_custom_parameters(
#    current_parameters: Optional[Parameters],
#    provided_parameters: Optional[ParametersWithoutCustom]
#) -> Parameters:
#    """Return a Parameters object by merging defaults with provided non-custom values."""
#    # Initialize to default if current is None
#    if current_parameters is None:
#        current_parameters = Parameters(
#            start_datetime=datetime.now(),
#            end_datetime=datetime.now() - timedelta(days=365),
#            symbol="",
#            timeframe="60m",
#            margin=0.5,
#            custom_parameters={}
#        )
#
#    if provided_parameters is not None:
#        for param_name in ['start_datetime', 'end_datetime', 'symbol', 'timeframe', 'margin']:
#            value = getattr(provided_parameters, param_name, None)
#            if value is not None:
#                setattr(current_parameters, param_name, value)
#
#    return current_parameters
#
#def merge_custom_parameters(
#    base_custom: dict,
#    override_custom: Optional[dict]
#) -> dict:
#    """Return a new custom_parameters dict merged from base and override."""
#    merged = base_custom.copy()
#    if override_custom:
#        merged.update(override_custom)
#    return merged
#
#from tester_framework.test_deck import GUIManager
#
## Example snippet implementation
#def analysis_snippet(configurations, parameters):
#    """Example processing function with config and parameters."""
#    return {
#        "time_range": {
#            "start": configurations["startDatetime"],
#            "end": configurations["endDateTime"]
#        },
#        "metrics": {
#            "param1": parameters.get("threshold", 0.5),
#            "calculation": f"Result using {parameters.get('method', 'default')}"
#        }
#    }
#
## Create and configure the manager
#guim = GUIManager()
#guim.register(
#    snippet=analysis_snippet,
#    configurations={
#        "startDatetime": "2023-01-01T00:00",
#        "endDateTime": "2023-01-02T00:00"
#    },
#    parameters= [
#        {"name": "linear" , "type": "string", "value": "default"},
#    ]
#)
#
## Start the server on port 5000
#guim.start()
#--- TMP ---#
#from sys import path
#import os
#path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
##--- END TMP ---#
#import importlib.util
#from datetime import datetime, timedelta
#import os
#import hashlib
#import json
#from models import Parameters, Session, TestSandbox
#print(path)
#
#def set_strategies_dir(directory: str) -> None:
#    """Set the directory for strategy files."""
#    global strategies_directory
#    strategies_directory = directory
#
## Function to dynamically load a Python script file
#def load_script(filename):
#    spec = importlib.util.spec_from_file_location("module.name", filename)
#    module = importlib.util.module_from_spec(spec)
#    spec.loader.exec_module(module)
#    return module
#
## Create the .sandboxes folder if it doesn't exist
#if not os.path.exists(".sandboxes"):
#    os.makedirs(".sandboxes")
#
## Function to create a sandbox class from a strategy script
#def create_sandbox_class(strategy_name, main_func, custom_parameters, default_parameters, symbols, timeframes):
#    # Define the sandbox class structure
#    class Sandbox:
#        def __init__(self, name: str, logic: callable, supported_timeframes: list, supported_symbols: list):
#            self.name = name
#            self.logic = logic
#            self.supported_timeframes = supported_timeframes
#            self.supported_symbols = supported_symbols
#            self.parameters = Parameters(
#                start_datetime=datetime.now() - timedelta(days=365),
#                end_datetime=datetime.now(),
#                symbol="",
#                timeframe="60m",
#                margin=0.5,
#                custom_parameters=custom_parameters
#            )
#            self.locked_parameters = {
#                'start_datetime': False,
#                'end_datetime': False,
#                'symbol': False,
#                'timeframe': False,
#                'margin': False,
#                'custom_parameters': False
#            }
#        
#        def run(self):
#            session = self.logic(self.parameters)
#            return session
#
#    # Save the sandbox class in a file
#    sandbox_filename = f".sandboxes/{strategy_name}_sandbox.py"
#    with open(sandbox_filename, "w") as f:
#        f.write(f"""from datetime import datetime, timedelta
#from strategy_tester_framework import Parameters, Session
#
#class {strategy_name}Sandbox:
#    def __init__(self, name: str, logic: callable, supported_timeframes: list, supported_symbols: list):
#        self.name = name
#        self.logic = logic
#        self.supported_timeframes = supported_timeframes
#        self.supported_symbols = supported_symbols
#        self.parameters = Parameters(
#            start_datetime=datetime.now() - timedelta(days=365),
#            end_datetime=datetime.now(),
#            symbol="",
#            timeframe="60m",
#            margin=0.5,
#            custom_parameters={custom_parameters}
#        )
#        self.locked_parameters = {{
#            'start_datetime': False,
#            'end_datetime': False,
#            'symbol': False,
#            'timeframe': False,
#            'margin': False
#        }}
#    
#    def run(self):
#        session = self.logic(self.parameters)
#        return session
#""")
#    
#    print(f"Sandbox class for {strategy_name} saved as {sandbox_filename}")
#    
#    # Return the sandbox class
#    return Sandbox(strategy_name, main_func, timeframes, symbols)
#
## Main function to iterate over strategy files and generate sandboxes
#def generate_sandboxes():
#    for filename in os.listdir(strategies_directory):
#        if filename.endswith(".py"):
#            script_path = os.path.join(strategies_directory, filename)
#            module = load_script(script_path)
#            
#            strategy_name = filename[:-3]  # Strip '.py' to get the name
#            if hasattr(module, 'main') and callable(module.main):
#                main_func = module.main
#                custom_parameters = getattr(module, 'custom_parameters', {})
#                default_parameters = getattr(module, 'default_parameters', {})
#                symbols = getattr(module, 'supported_symbols', [])
#                timeframes = getattr(module, 'supported_timeframes', [])
#                locked_parameters = getattr(module, 'locked_parameters', {})
#                
#                # Create the sandbox class
#                sandbox_class = create_sandbox_class(strategy_name, main_func, custom_parameters, default_parameters, symbols, timeframes)
#
#                # Optionally return or store sandbox_class
#                print(f"Sandbox class for strategy {strategy_name} generated.")
#
## Run the process to create sandboxes
#set_strategies_dir("strategies/")  # Set the directory for strategy files
#generate_sandboxes()
#
#
#
#
## Define the directory to look for strategy files
#strategies_directory = "strategies/"
#
## Function to calculate the checksum (SHA256) of a file
#def get_file_checksum(file_path):
#    sha256_hash = hashlib.sha256()
#    with open(file_path, "rb") as f:
#        # Read file in chunks to handle large files
#        for byte_block in iter(lambda: f.read(4096), b""):
#            sha256_hash.update(byte_block)
#    return sha256_hash.hexdigest()
#
## Function to generate checksums for all strategy files
#def generate_checksums():
#    checksums = {}
#    
#    for filename in os.listdir(strategies_directory):
#        if filename.endswith(".py"):
#            file_path = os.path.join(strategies_directory, filename)
#            checksum = get_file_checksum(file_path)
#            checksums[filename] = checksum
#    
#    # Save the current checksums to a file
#    with open("checksums.json", "w") as f:
#        json.dump(checksums, f, indent=4)
#    
#    print("Checksums generated and saved to checksums.json")
#
## Function to compare current checksums with the stored ones
#def compare_checksums():
#    current_checksums = {}
#    
#    # Calculate current checksums for all strategy files
#    for filename in os.listdir(strategies_directory):
#        if filename.endswith(".py"):
#            file_path = os.path.join(strategies_directory, filename)
#            checksum = get_file_checksum(file_path)
#            current_checksums[filename] = checksum
#    
#    # Load the previous checksums from the file
#    if os.path.exists("checksums.json"):
#        with open("checksums.json", "r") as f:
#            previous_checksums = json.load(f)
#    else:
#        previous_checksums = {}
#    
#    # Compare current checksums with the previous ones
#    changes_detected = False
#    for filename, checksum in current_checksums.items():
#        if filename not in previous_checksums or previous_checksums[filename] != checksum:
#            print(f"Change detected in file: {filename}")
#            changes_detected = True
#    
#    if not changes_detected:
#        print("No changes detected in strategy files.")
#    
#    # Optionally, update the checksum file if changes are detected
#    if changes_detected:
#        with open("checksums.json", "w") as f:
#            json.dump(current_checksums, f, indent=4)
#        print("Checksums updated in checksums.json")
#
## Call the function to generate or compare checksums
## To generate initial checksums:
## generate_checksums()
#
## To compare current checksums with previous ones:
#compare_checksums()
#