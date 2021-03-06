from openslides.core.config import ConfigVariable, config
from openslides.core.exceptions import ConfigError, ConfigNotFound
from openslides.utils.test import TestCase


class TestConfigException(Exception):
    pass


class HandleConfigTest(TestCase):
    def setUp(self):
        # Save the old value of the config object and add the test values
        # TODO: Can be changed to setUpClass when Django 1.8 is no longer supported
        self._config_values = config.config_variables.copy()
        config.update_config_variables(set_grouped_config_view())
        config.update_config_variables(set_simple_config_view())
        config.update_config_variables(set_simple_config_view_multiple_vars())
        config.update_config_variables(set_simple_config_collection_disabled_view())
        config.update_config_variables(set_simple_config_collection_with_callback())

    def tearDown(self):
        # Reset the config variables
        config.config_variables = self._config_values

    def get_config_var(self, key):
        return config[key]

    def set_config_var(self, key, value):
        config[key] = value

    def test_get_config_default_value(self):
        self.assertEqual(config['string_var'], 'default_string_rien4ooCZieng6ah')
        self.assertTrue(config['bool_var'])
        self.assertEqual(config['integer_var'], 3)
        self.assertEqual(config['choices_var'], '1')
        self.assertEqual(config['none_config_var'], None)
        with self.assertRaisesMessage(
                ConfigNotFound,
                'The config variable unknown_config_var was not found.'):
            self.get_config_var('unknown_config_var')

    def test_get_multiple_config_var_error(self):
        with self.assertRaisesMessage(
                ConfigError,
                'Too many values for config variable multiple_config_var found.'):
            config.update_config_variables(set_simple_config_view_multiple_vars())

    def test_setup_config_var(self):
        self.assertRaises(TypeError, ConfigVariable)
        self.assertRaises(TypeError, ConfigVariable, name='foo')
        self.assertRaises(TypeError, ConfigVariable, default_value='foo')

    def test_change_config_value(self):
        self.assertEqual(config['string_var'], 'default_string_rien4ooCZieng6ah')
        config['string_var'] = 'other_special_unique_string dauTex9eAiy7jeen'
        self.assertEqual(config['string_var'], 'other_special_unique_string dauTex9eAiy7jeen')

    def test_missing_cache_(self):
        self.assertEqual(config['string_var'], 'default_string_rien4ooCZieng6ah')

    def test_config_contains(self):
        self.assertTrue('string_var' in config)
        self.assertFalse('unknown_config_var' in config)

    def test_set_value_before_getting_it(self):
        """
        Try to call __setitem__ before __getitem__.
        """
        config['additional_config_var'] = 'value'

    def test_on_change(self):
        """
        Tests that the special callback is called and raises a special
        message.
        """
        with self.assertRaisesMessage(
                TestConfigException,
                'Change callback dhcnfg34dlg06kdg successfully called.'):
            self.set_config_var(
                key='var_with_callback_ghvnfjd5768gdfkwg0hm2',
                value='new_string_kbmbnfhdgibkdjshg452bc')

        self.assertEqual(
            config['var_with_callback_ghvnfjd5768gdfkwg0hm2'],
            'new_string_kbmbnfhdgibkdjshg452bc')


def set_grouped_config_view():
    """
    Sets a grouped config collection. There are some variables, one variable
    with a string as default value, one with a boolean as default value,
    one with an integer as default value, one with choices and one hidden
    variable. These variables are grouped in two subgroups.
    """
    yield ConfigVariable(
        name='string_var',
        default_value='default_string_rien4ooCZieng6ah',
        group='Config vars for testing 1',
        subgroup='Group 1 aiYeix2mCieQuae3')
    yield ConfigVariable(
        name='bool_var',
        default_value=True,
        input_type='boolean',
        group='Config vars for testing 1',
        subgroup='Group 1 aiYeix2mCieQuae3')
    yield ConfigVariable(
        name='integer_var',
        default_value=3,
        input_type='integer',
        group='Config vars for testing 1',
        subgroup='Group 1 aiYeix2mCieQuae3')

    yield ConfigVariable(
        name='hidden_var',
        default_value='hidden_value',
        group='Config vars for testing 1',
        subgroup='Group 2 Toongai7ahyahy7B')
    yield ConfigVariable(
        name='choices_var',
        default_value='1',
        input_type='choice',
        choices=(
            {'value': '1', 'display_name': 'Choice One Ughoch4ocoche6Ee'},
            {'value': '2', 'display_name': 'Choice Two Vahnoh5yalohv5Eb'}),
        group='Config vars for testing 1',
        subgroup='Group 2 Toongai7ahyahy7B')


def set_simple_config_view():
    """
    Sets a simple config view with some config variables but without
    grouping.
    """
    yield ConfigVariable(name='additional_config_var', default_value='BaeB0ahcMae3feem')
    yield ConfigVariable(name='additional_config_var_2', default_value='')
    yield ConfigVariable(name='none_config_var', default_value=None)


def set_simple_config_view_multiple_vars():
    """
    Sets a bad config view with some multiple config vars.
    """
    yield ConfigVariable(name='multiple_config_var', default_value='foobar1')
    yield ConfigVariable(name='multiple_config_var', default_value='foobar2')


def set_simple_config_collection_disabled_view():
    yield ConfigVariable(name='hidden_config_var_2', default_value='')


def set_simple_config_collection_with_callback():
    def callback():
        raise TestConfigException('Change callback dhcnfg34dlg06kdg successfully called.')
    yield ConfigVariable(
        name='var_with_callback_ghvnfjd5768gdfkwg0hm2',
        default_value='',
        on_change=callback)
