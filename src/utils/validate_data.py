import great_expectations as gx
from typing import Tuple, List

def validate_telco_data(df) -> Tuple[bool, List[str]]:
    """
    Comprehensive data validation for Telco Customer Churn dataset using GX 1.0+.
    """
    print("🔍 Starting data validation with Great Expectations 1.0+...")
    
    # 1. Initialize an Ephemeral Data Context
    context = gx.get_context()
    
    # 2. Setup Data Source and Asset
    # Using 'add_or_update' ensures the script is idempotent (can run multiple times)
    data_source = context.data_sources.add_or_update_pandas(name="telco_source")
    data_asset = data_source.add_dataframe_asset(name="telco_asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("telco_batch_def")
    
    # 3. Create the Expectation Suite
    suite = gx.ExpectationSuite(name="telco_validation_suite")
    
    # Define Expectations
    expectations = [
        # Schema / Existence
        gx.expectations.ExpectColumnToExist(column="customerID"),
        gx.expectations.ExpectColumnValuesToNotBeNull(column="customerID"),
        gx.expectations.ExpectColumnToExist(column="gender"),
        gx.expectations.ExpectColumnToExist(column="Contract"),
        gx.expectations.ExpectColumnToExist(column="tenure"),
        gx.expectations.ExpectColumnToExist(column="MonthlyCharges"),
        gx.expectations.ExpectColumnToExist(column="TotalCharges"),
        
        # Business Logic / Categorical
        gx.expectations.ExpectColumnValuesToBeInSet(column="gender", value_set=["Male", "Female"]),
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Contract", 
            value_set=["Month-to-month", "One year", "Two year"]
        )
        
    ]
    
    for exp in expectations:
        suite.add_expectation(exp)
        
    # 4. REGISTER the suite to the context
    suite = context.suites.add_or_update(suite)
    
    # 5. Create and REGISTER the Validation Definition
    validation_definition = gx.ValidationDefinition(
        name="telco_validation_def",
        data=batch_definition,
        suite=suite
    )
    validation_definition = context.validation_definitions.add_or_update(validation_definition)
    
    # 6. Run Validation
    print("   ⚙️  Running complete validation suite...")
    results = validation_definition.run(batch_parameters={"dataframe": df})
    
    # 7. Process Results
    failed_expectations = []
    for res in results.results:
        if not res.success:
            # New API uses .expectation_config.type
            failed_expectations.append(res.expectation_config.type)
    
    total_checks = len(results.results)
    passed_checks = total_checks - len(failed_expectations)
    
    if results.success:
        print(f"✅ Data validation PASSED: {passed_checks}/{total_checks} checks successful")
    else:
        print(f"❌ Data validation FAILED: {len(failed_expectations)}/{total_checks} checks failed")
        print(f"   Failed types: {list(set(failed_expectations))}")
    
    return results.success, failed_expectations
