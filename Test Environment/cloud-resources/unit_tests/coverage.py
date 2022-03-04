"""
This script correlates test use cases with inspec and KCC templates to determine
unit test coverage based on information available in test suite definition.
Command line parameters: <unit test definiion file>
The logic: collects information from enabled unit test cases setting aside
inspec and kcc templates. Compares full list of inspec and kcc templates
files against those associated with unit test cases.
"""
import os
import sys
from glob import glob
import yaml #pylint: disable=import-error

INSPEC_CONTROLS_LOCATION = 'inspec/controls'
KCC_TEMPLATES_LOCATION = 'templates/gcp-project'


def list_all_unit_tests(base_dir):
    """
    Returns list of unit tests in base_dir
    """
    result = list()
    files = os.listdir(base_dir)
    for item in files:
        if os.path.isdir(os.path.join(base_dir, item))  and item[0] != '_':
            result.append(item)
    return result

def load_deps(home, cases):
    """
    returns lists (sets) of inspec controls and kcc templates associated with test cases
    """
    unit_cases = set()
    inspec_controls = set()
    kcc_templates = set()
    if cases == 'all':
        unit_cases = list_all_unit_tests(home)
    else:
        unit_cases = cases.split(',')

    for case in unit_cases:
        try:
            with  open(os.path.join(home, case, 'definition.yml')) as f_in:
                try:
                    definition = yaml.safe_load(f_in)
                    # pragma pylint: disable=C0301
                    tmp_inspec_controls = [os.path.basename(item) for item in definition['inspecControls']]
                    tmp_templates = [os.path.basename(item) for item in definition['kccTemplates']]
                    for item in tmp_inspec_controls:
                        inspec_controls.add(item)
                    for item in tmp_templates:
                        kcc_templates.add(item)
                except yaml.YAMLError:
                    pass
        except FileNotFoundError:
            pass
    return (inspec_controls, kcc_templates)

def process(test_suites):
    """
    Received test suite definition, loads associated use cases, aggregates associated files
    and prints results.
    """
    covered_inspec = set()
    covered_kcc = set()
    suites = test_suites['unitTestSuits']
    for suite in suites:
        cases = suite['cases']
        home = suite['homeDir']
        tmp_inspec = set()
        tmp_kcc_templates = set()
        tmp_inspec, tmp_kcc_templates = load_deps(home, cases)
        covered_inspec |= tmp_inspec
        covered_kcc |= tmp_kcc_templates

    # pragma pylint: disable=C0301
    all_inspec = [os.path.basename(item) for item in glob(os.path.join(INSPEC_CONTROLS_LOCATION, '*.rb'))]
    all_kcc = [os.path.basename(item) for item in glob(os.path.join(KCC_TEMPLATES_LOCATION, '*.j2'))]

    # Print results...
    k_coverage = float(len(covered_kcc))/float(len(all_kcc))
    print("\n--------------------------------------------------------------")
    print("**** KCC Templates Coverage: {:.0%} ****".format(k_coverage))
    print("--------------------------------------------------------------")
    for item in all_kcc:
        if item in covered_kcc:
            print("{}: OK".format(item))
        else:
            print("{} NOT COVERED".format(item))
    i_coverage = float(len(covered_inspec))/float(len(all_inspec))
    print("\n--------------------------------------------------------------")
    print("**** Inspec Controls Coverage: {:.0%} ****".format(i_coverage))
    print("--------------------------------------------------------------")
    for item in all_inspec:
        if item in covered_inspec:
            print("{}: OK".format(item))
        else:
            print("{} NOT COVERED".format(item))

def main():
    """
    Main entry point.
    Single parameter is expected: <unit test suite definition filename >
    """
    suite_def = sys.argv[1]
    with open(suite_def) as f_in:
        test_suites = yaml.safe_load(f_in)
        process(test_suites)

if __name__ == "__main__":
    main()
