# -*- encoding: utf-8 -*-
import dsl
from . import FixtureTest


class ShieldTextLengthTest(FixtureTest):

    # this is real data. For the rest of the tests, it will be modified
    def test_create_shield_text_length(self):
        import dsl

        z, x, y = (16, 10470, 25340)

        self.generate_fixtures(
            # https://www.openstreetmap.org/way/417097119
            dsl.way(417097119, dsl.tile_diagonal(z, x, y), {
                'cycleway:right': 'lane',
                'hgv': 'designated',
                'hgv:state_network': 'yes',
                'highway': 'primary',
                'lanes': '2',
                'lcn_ref': '50',
                'maxspeed': '35 mph',
                'name': 'Sloat Boulevard',
                'name:etymology:wikidata': 'Q634931',
                'oneway': 'yes',
                'ref': 'CA 35',
                'sidewalk': 'right',
                'source': 'openstreetmap.org',
                'source:hgv:state_network': 'Caltrans http://www.dot.ca.gov/hq/traffops/trucks/truckmap/',
                'tiger:cfcc': 'A45',
                'tiger:county': 'San Francisco, CA',
                'tiger:name_base': 'Sloat',
                'tiger:name_type': 'Blvd',
            }),
            dsl.relation(1976278, {
                'network': 'US:CA',
                'ref': '35',
                'route': 'road',
                'source': 'openstreetmap.org',
                'type': 'route',
            }, ways=[417097119]),
            dsl.relation(32312, {
                'cycle_network': 'US:CA:SF',
                'network': 'lcn',
                'ref': '50',
                'source': 'openstreetmap.org',
                'route': 'bicycle',
                'type': 'route',
            }, ways=[417097119]),
            dsl.relation(3002741, {
                'network': 'Muni',
                'ref': '23',
                'route': 'bus',
                'source': 'openstreetmap.org',
                'type': 'route',
            }, ways=[417097119])
        )

        self.assert_has_feature(
            z, x, y, 'roads', {
                'id': 417097119,
                'shield_text': '35',
                'shield_text_length': '2',
                'bicycle_shield_text': '50',
                'bicycle_shield_text_length': '2',
                'bus_shield_text': '23',
                'bus_shield_text_length': '2'
            })

    def test_shield_text_length_is_a_string(self):
        import dsl

        z, x, y = (16, 10470, 25340)

        self.generate_fixtures(
            # https://www.openstreetmap.org/way/417097119
            dsl.way(417097119, dsl.tile_diagonal(z, x, y), {
                'cycleway:right': 'lane',
                'hgv': 'designated',
                'hgv:state_network': 'yes',
                'highway': 'primary',
                'lanes': '2',
                'lcn_ref': '50',
                'maxspeed': '35 mph',
                'name': 'Sloat Boulevard',
                'name:etymology:wikidata': 'Q634931',
                'oneway': 'yes',
                'ref': 'CA 35',
                'sidewalk': 'right',
                'source': 'openstreetmap.org',
                'source:hgv:state_network': 'Caltrans http://www.dot.ca.gov/hq/traffops/trucks/truckmap/',
                'tiger:cfcc': 'A45',
                'tiger:county': 'San Francisco, CA',
                'tiger:name_base': 'Sloat',
                'tiger:name_type': 'Blvd',
            }),
            dsl.relation(1976278, {
                'network': 'US:CA',
                'ref': '35',
                'route': 'road',
                'source': 'openstreetmap.org',
                'type': 'route',
            }, ways=[417097119]),
            dsl.relation(32312, {
                'cycle_network': 'US:CA:SF',
                'network': 'lcn',
                'ref': '50',
                'source': 'openstreetmap.org',
                'route': 'bicycle',
                'type': 'route',
            }, ways=[417097119]),
            dsl.relation(3002741, {
                'network': 'Muni',
                'ref': '23',
                'route': 'bus',
                'source': 'openstreetmap.org',
                'type': 'route',
            }, ways=[417097119])
        )

        self.assert_no_matching_feature(z, x, y, 'roads', {'id': 417097119, 'shield_text_length': 2})

    # make fields with text that is too long.  Make sure things are still correct
    def test_lengths_over_6_or_empty_are_not_reported(self):
        import dsl

        z, x, y = (16, 10470, 25340)

        self.generate_fixtures(
            # https://www.openstreetmap.org/way/417097119
            dsl.way(417097119, dsl.tile_diagonal(z, x, y), {
                'cycleway:right': 'lane',
                'hgv': 'designated',
                'hgv:state_network': 'yes',
                'highway': 'primary',
                'lanes': '2',
                'lcn_ref': '50',
                'maxspeed': '35 mph',
                'name': 'Sloat Boulevard',
                'name:etymology:wikidata': 'Q634931',
                'oneway': 'yes',
                'ref': 'CA 35',
                'sidewalk': 'right',
                'source': 'openstreetmap.org',
                'source:hgv:state_network': 'Caltrans http://www.dot.ca.gov/hq/traffops/trucks/truckmap/',
                'tiger:cfcc': 'A45',
                'tiger:county': 'San Francisco, CA',
                'tiger:name_base': 'Sloat',
                'tiger:name_type': 'Blvd',
            }),
            dsl.relation(1976278, {
                'network': 'US:CA',
                'ref': '123456',
                'route': 'road',
                'source': 'openstreetmap.org',
                'type': 'route',
            }, ways=[417097119]),
            dsl.relation(32312, {
                'cycle_network': 'US:CA:SF',
                'network': 'lcn',
                'ref': '1234567',
                'source': 'openstreetmap.org',
                'route': 'bicycle',
                'type': 'route',
            }, ways=[417097119]),
            dsl.relation(3002741, {
                'network': 'Muni',
                'ref': '',
                'route': 'bus',
                'source': 'openstreetmap.org',
                'type': 'route',
            }, ways=[417097119])
        )

        self.assert_has_feature(
            z, x, y, 'roads', {
                'id': 417097119,
                'shield_text': '123456',
                'shield_text_length': '6',
                'bicycle_shield_text': '1234567',
                'bus_shield_text': '',
            })

        self.assert_no_matching_feature(z, x, y, 'roads', {
            'id': 417097119, 'bicycle_shield_text_length': '7', 'bus_shield_text_length': '0'})