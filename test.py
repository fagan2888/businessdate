# -*- coding: utf-8 -*-

#  businessdate
#  -----------
#  A fast, efficient Python library for generating business dates inherited
#  from float for fast date operations. Typical banking business methods
#  are provided like business holidays adjustment, day count fractions.
#  Beside dates generic business periods offer to create time periods like
#  '10Y', '3 Months' or '2b'. Periods can easily added to business dates.
#
#  Author:  pbrisk <pbrisk_at_github@icloud.com>
#  Website: https://github.com/pbrisk/businessdate
#  License: APACHE Version 2 License (see LICENSE file)

import os
import unittest

from datetime import datetime, date, timedelta

from businessdate.methods.holidays import easter, target_days
from businessdate.methods.ymd import from_ymd_to_excel, from_excel_to_ymd
from businessdate.basedate import BaseDate
from businessdate import BusinessDate, BusinessPeriod, BusinessRange, BusinessSchedule, BusinessHolidays


class BaseDateUnitTest(unittest.TestCase):
    def setUp(self):
        self.pairs = list()  # to store date(as string), exceldate[int](as string)
        f = open("test_data/excel_date_test_data.csv")
        for line in f:
            self.pairs.append(line.split(';'))
        f.close()

    def test_from_ymd_to_excel(self):
        for pair in self.pairs:
            d, m, y = [int(part) for part in pair[0].split('.')]
            i = int(pair[1])
            self.assertEqual(i, from_ymd_to_excel(y, m, d))

    def test_from_excel_to_ymd(self):
        for pair in self.pairs:
            d, m, y = [int(part) for part in pair[0].split('.')]
            i = int(pair[1])
            self.assertEqual((y, m, d), from_excel_to_ymd(i))

    def test_base_date(self):
        BusinessDate.BASE_DATE = '20160606'
        self.assertEqual(BusinessDate(), BusinessDate('20160606'))
        BusinessDate.BASE_DATE = date.today()


class DayCountUnitTests(unittest.TestCase):
    # n(ame) cor(respondence)
    # correspondence between dcc and the functions
    ncor = {'30/360': 'get_30_360',
            'ACT/360': 'get_act_360',
            'ACT/365': 'get_act_365',
            '30E/360': 'get_30e_360',
            'ACT/ACT': 'get_act_act',
            'ACT/365.25': 'get_act_36525'
            }

    def setUp(self):
        self.testfile = open('test_data/daycount_test_data.csv')
        self.header = self.testfile.readline().rstrip().split(';')
        self.test_data = list()
        for line in self.testfile:
            self.test_data.append(line.rstrip().split(';'))
        self.startdate_idx = self.header.index('StartDate')
        self.enddate_idx = self.header.index('EndDate')

    def test_get_30_360(self):
        methodname = '30/360'
        method_idx = self.header.index(methodname)
        f = BusinessDate.__dict__[DayCountUnitTests.ncor[methodname]]
        for data in self.test_data:
            start_date = BusinessDate(data[self.startdate_idx])
            end_date = BusinessDate(data[self.enddate_idx])
            self.assertAlmostEqual(f(start_date, end_date), float(data[method_idx]))

    def test_get_30E_360(self):
        methodname = '30E/360'
        method_idx = self.header.index(methodname)
        f = BusinessDate.__dict__[DayCountUnitTests.ncor[methodname]]
        for data in self.test_data:
            start_date = BusinessDate(data[self.startdate_idx])
            end_date = BusinessDate(data[self.enddate_idx])
            self.assertAlmostEqual(f(start_date, end_date), float(data[method_idx]))

    def test_get_act_act(self):
        methodname = 'ACT/ACT'
        method_idx = self.header.index(methodname)
        f = BusinessDate.__dict__[DayCountUnitTests.ncor[methodname]]
        for data in self.test_data:
            start_date = BusinessDate(data[self.startdate_idx])
            end_date = BusinessDate(data[self.enddate_idx])
            self.assertAlmostEqual(f(start_date, end_date), float(data[method_idx]))

    def test_get_ACT_360(self):
        methodname = 'ACT/360'
        method_idx = self.header.index(methodname)
        f = BusinessDate.__dict__[DayCountUnitTests.ncor[methodname]]
        for data in self.test_data:
            start_date = BusinessDate(data[self.startdate_idx])
            end_date = BusinessDate(data[self.enddate_idx])
            self.assertAlmostEqual(f(start_date, end_date), float(data[method_idx]))

    def test_get_ACT_365(self):
        methodname = 'ACT/365'
        method_idx = self.header.index(methodname)
        f = BusinessDate.__dict__[DayCountUnitTests.ncor[methodname]]
        for data in self.test_data:
            start_date = BusinessDate(data[self.startdate_idx])
            end_date = BusinessDate(data[self.enddate_idx])
            self.assertAlmostEqual(f(start_date, end_date), float(data[method_idx]))

    def test_get_ACT_36525(self):
        methodname = 'ACT/365.25'
        method_idx = self.header.index(methodname)
        f = BusinessDate.__dict__[DayCountUnitTests.ncor[methodname]]
        for data in self.test_data:
            start_date = BusinessDate(data[self.startdate_idx])
            end_date = BusinessDate(data[self.enddate_idx])
            self.assertAlmostEqual(f(start_date, end_date), float(data[method_idx]))


class BusinessHolidaysUnitTests(unittest.TestCase):
    def setUp(self):
        self.holidays = BusinessHolidays(target_days(2016))
        self.easter = dict()
        self.easter[2015] = date(2015, 4, 5)
        self.easter[2016] = date(2016, 3, 27)
        self.easter[2017] = date(2017, 4, 16)
        self.easter[2018] = date(2018, 4, 1)
        self.easter[2019] = date(2019, 4, 21)
        self.easter[2020] = date(2020, 4, 12)
        self.target = dict()
        for y in self.easter:
            self.target[y] = [date(y, 1, 1), date(y, 5, 1), date(y, 12, 25), date(y, 12, 26)]
            self.target[y].append(self.easter[y] - timedelta(2))
            self.target[y].append(self.easter[y] + timedelta(1))

    def test_easter(self):
        for y in self.easter:
            self.assertEqual(easter(y), self.easter[y])

    def test_target_days(self):
        for y in self.target:
            t = target_days(y)
            d = date(y, 1, 1) - timedelta(1)
            while d < date(y + 1, 1, 1):
                if d in self.target[y]:
                    self.assertTrue(d in t)
                else:
                    self.assertTrue(d not in t)
                d += timedelta(1)

    def test_business_holidays(self):
        self.assertTrue(BusinessDate(20160101).to_date() in self.holidays)
        self.assertFalse(BusinessDate(20160102).to_date() in self.holidays)
        self.assertTrue(BusinessDate(20160102).to_date() not in self.holidays)
        self.assertTrue(BusinessDate(20160325).to_date() in self.holidays)
        self.assertTrue(BusinessDate(20160328).to_date() in self.holidays)
        self.assertTrue(BusinessDate(20160501).to_date() in self.holidays)


class BusinessDateUnitTests(unittest.TestCase):
    def setUp(self):
        self.jan29_15 = BusinessDate(20150129)
        self.feb28_15 = BusinessDate(20150228)
        self.dec31_15 = BusinessDate(20151231)
        self.jan01 = BusinessDate(20160101)
        self.jan02 = BusinessDate(20160102)
        self.jan04 = BusinessDate(20160104)
        self.jan29 = BusinessDate(20160129)
        self.jan31 = BusinessDate(20160131)
        self.feb01 = BusinessDate(20160201)
        self.feb28 = BusinessDate(20160228)
        self.feb29 = BusinessDate(20160229)
        self.mar31 = BusinessDate(20160331)
        self.jun30 = BusinessDate(20160630)
        self.sep30 = BusinessDate(20160930)

        self.dates = [self.jan29_15, self.feb28_15, self.dec31_15,
                      self.jan01, self.jan02, self.jan04, self.jan29, self.jan31,
                      self.feb01, self.feb28, self.feb29, self.mar31, self.jun30, self.sep30]

    def test_constructors(self):
        self.assertEqual(BusinessDate(date.today()), BusinessDate())
        self.assertEqual(self.jan02, BusinessDate('2016-01-02'))
        self.assertEqual(self.jan02, BusinessDate('01/02/2016'))
        self.assertEqual(self.jan02, BusinessDate('02.01.2016'))
        self.assertEqual(self.jan02, BusinessDate(42371))
        self.assertEqual(self.jan02, BusinessDate(42371.0))
        self.assertEqual([self.jan01, self.jan02], BusinessDate([20160101, 42371]))

    def test_to_string(self):
        self.assertEqual(self.jan02, BusinessDate(str(self.jan02)))
        self.assertEqual(str(self.jan02), '20160102')
        self.assertEqual(repr(self.jan02), "BusinessDate('20160102')")
        self.assertEqual(str(BusinessDate(42371)), '20160102')
        self.assertEqual(self.jan02, eval(repr(self.jan02)))

    def test_properties(self):
        self.assertEqual(self.jan01.day, 1)
        self.assertEqual(self.jan01.month, 1)
        self.assertEqual(self.jan01.year, 2016)

    def test_operators(self):
        self.assertEqual(self.jan01 + '2D', self.jan02 + '1D')
        self.assertEqual(self.jan01 - '1D', self.jan02 - '2D')
        self.assertEqual(self.jan02 - '1D' + '1M', self.feb01)
        self.assertRaises(TypeError, lambda: '1D' + self.jan02)
        self.assertEqual(self.jan01 - BusinessPeriod('1D'), self.jan02 - '2D')
        self.assertRaises(TypeError, lambda: BusinessPeriod('1D') + self.jan02)
        self.assertRaises(TypeError, lambda: BusinessPeriod('1D') - self.jan01)
        self.assertEqual(self.dec31_15.add_period(BusinessPeriod('2B'), BusinessHolidays()),
                         self.dec31_15.add_period(BusinessPeriod('2B'), BusinessHolidays([self.jan02])))

    def test_validations(self):
        # self.assertTrue(BusinessDate.is_businessdate(18991229))
        self.assertTrue(BusinessDate.is_businessdate(19000102))
        self.assertTrue(BusinessDate.is_businessdate(20160131))
        self.assertTrue(BusinessDate.is_businessdate(20160228))
        self.assertTrue(BusinessDate.is_businessdate(20160229))
        self.assertFalse(BusinessDate.is_businessdate(20160230))
        self.assertFalse(BusinessDate.is_businessdate(20160231))
        self.assertTrue(BusinessDate.is_businessdate(20150228))
        self.assertFalse(BusinessDate.is_businessdate(20150229))
        self.assertFalse(BusinessDate.is_businessdate('xyz'))
        self.assertFalse(BusinessDate.is_businessdate(-125))
        self.assertFalse(BusinessDate.is_businessdate(-20150228))

    def test_calculations(self):
        self.assertEqual(self.jan01.add_days(1), self.jan02)
        self.assertEqual(self.jan01.add_months(1), self.feb01)
        self.assertEqual(str(self.jan01.add_years(1)), '20170101')
        self.assertEqual(self.jan01.add_period('2D'), self.jan02 + BusinessPeriod('1D'))
        self.assertEqual(self.jan02.add_period('-2D'), self.jan01 - BusinessPeriod('1D'))
        self.assertEqual(self.jan02.add_period('-1b'), self.jan01 - BusinessPeriod('1b'))
        self.assertNotEqual(BusinessDate(20160630).add_period(BusinessPeriod('2B')),
                            BusinessDate(20160630).add_period(BusinessPeriod('2B'), BusinessHolidays(['20160704'])))
        self.assertEqual(self.jan01 + '1b', self.jan02 + '1b')

        d, p = BusinessDate('20160229'), BusinessPeriod('1Y1M1D')
        self.assertEqual((d + p - d), p, (d + p - d, d, p, d + p))
        d, p = BusinessDate('20150129'), BusinessPeriod('1Y2M1D')
        self.assertEqual((d + p - d), p, (d + p - d, d, p, d + p))
        d, p = BusinessDate('20150129'), BusinessPeriod('1Y1M1D')
        self.assertEqual((d + p - d), p, (d + p - d, d, p, d + p))
        # non idepotent pairs
        d, p = BusinessDate('20150129'), BusinessPeriod('1M29D')
        # self.assertEqual((d + p - d), p, (d + p - d, d, p, d + p))
        d, p = BusinessDate('20160129'), BusinessPeriod('1M29D')
        # self.assertEqual((d + p - d), p, (d + p - d, d, p, d + p))

        y, m, d = 5, 13, 66
        #y, m, d = 4, 4, 3
        periods = list()
        for y in range(y):
            for m in range(m):
                for d in range(d):
                    periods.append(BusinessPeriod(str(y) + 'y' + str(m) + 'm' + str(d) + 'd'))

        for d in self.dates:
            for p in periods:
                dp = d + p
                q = dp - d
                dq = d + q
                if p.days < 28:
                    self.assertEqual(q, p, (q, d, p, dp))
                elif p.days < 59 and not 28 <= p.days - q.days <= 32 and not q == p:
                    print d, p, dp, q
                # elif 59 <= p.days and not 28 <= p.days - q.days <= 32 and not q == p:
                #     print d, p, dp, q
                # only idempotent pairs work always (e.g. above)
                self.assertEqual(dq, dp, (dq, d, p, dp, q))
                self.assertEqual((dq - d), q, (dq - d, d, q, dq))

        d = BusinessDate(20160229)
        self.assertEqual(d + '1y' + '1m', BusinessDate(20170328))
        self.assertEqual(d + '1m' + '1y', BusinessDate(20170329))
        self.assertEqual(d + '1y1m', BusinessDate(20170329))

    def test_cast_to(self):
        self.assertTrue(isinstance(self.jan01.to_date(), date))
        self.assertTrue(isinstance(self.jan01, BusinessDate))
        self.assertTrue(isinstance(self.jan01-BusinessDate(), BusinessPeriod))
        self.assertTrue(isinstance(self.jan01.to_excel(), int))
        # removed ordinal support
        # self.assertTrue(isinstance(self.jan01.to_ordinal(), int))
        self.assertTrue(isinstance(str(self.jan01), str))
        self.assertTrue(isinstance(self.jan01.to_ymd(), tuple))

    def test_cast_from(self):
        for d in self.dates:
            self.assertEqual(BusinessDate(d.to_date()), d)
            self.assertEqual(d.__copy__(), d)
            self.assertEqual(BusinessDate(d.to_excel()), d)
            self.assertEqual(BusinessDate(str(d)), d)
            self.assertEqual(BusinessDate(*d.to_ymd()), d)

    def test_day_count(self):  # The daycount methods are also tested separately
        delta = float((self.mar31.to_date() - self.jan01.to_date()).days)
        total = float(((self.jan01 + '1y').to_date() - self.jan01.to_date()).days)

        self.assertAlmostEqual(self.jan01.get_day_count(self.mar31), delta / 365.25)
        self.assertAlmostEqual(self.jan01.get_day_count(self.mar31, 'ACT_36525'), delta / 365.25)
        self.assertAlmostEqual(self.jan01.get_day_count(self.mar31, '30_360'), 90. / 360.)
        self.assertAlmostEqual(self.jan01.get_day_count(self.mar31, 'ACT_ACT'), delta / total)

        self.assertAlmostEqual(self.jan01.get_30_360(self.mar31), 90. / 360.)
        self.assertAlmostEqual(self.jan01.get_act_360(self.mar31), delta / 360.)
        self.assertAlmostEqual(self.jan01.get_act_365(self.mar31), delta / 365.)
        self.assertAlmostEqual(self.jan01.get_act_36525(self.mar31), delta / 365.25)
        self.assertAlmostEqual(self.jan01.get_act_act(self.mar31), delta / total)

    def test_business_day_adjustment(self):
        self.assertEqual(self.jan01.adjust(), BusinessDate(20160101))
        self.assertEqual(self.jan01.adjust('NO'), BusinessDate(20160101))
        self.assertEqual(self.jan01.adjust('FOLLOW'), BusinessDate(20160104))

        self.assertEqual(self.jan01.adjust_follow(), BusinessDate(20160104))
        self.assertEqual(self.jan01.adjust_mod_follow(), BusinessDate(20160104))
        self.assertEqual(self.jan01.adjust_previous(), BusinessDate(20151231))
        self.assertEqual(self.jan01.adjust_mod_previous(), BusinessDate(20160104))
        self.assertEqual(self.jan01.adjust_start_of_month(), BusinessDate(20160104))
        self.assertEqual(self.jan01.adjust_end_of_month(), BusinessDate(20160129))
        self.assertEqual(self.jan01.adjust_imm(), BusinessDate(20160115))
        self.assertEqual(self.jan01.adjust_cds_imm(), BusinessDate(20160120))

    def test_business_day_is(self):
        self.assertFalse(self.jan01.is_business_day())
        self.assertTrue(BusinessDate(2016,1,1).is_leap_year())
        self.assertTrue(BusinessDate.is_businessdate('20160101'))
        self.assertFalse(BusinessDate.is_businessdate('ABC'))
        self.assertFalse(BusinessDate.is_businessdate('20160230'))
        self.assertTrue(BusinessDate.is_businessdate('20160229'))
        self.assertFalse(BusinessDate.is_businessdate('20150229'))

    def test_is_business_date(self):
        d = self.dec31_15
        holi = BusinessHolidays()
        bdate = BusinessDate.from_ymd(2016, 1, 1)
        is_bday_empty_calendar = bdate.is_business_day(holi)
        self.assertTrue(is_bday_empty_calendar)
        is_bday_default_calendar = bdate.is_business_day()
        self.assertFalse(is_bday_default_calendar)

        target_a = BusinessDate.from_ymd(2016, 1, 4)
        a = d.add_business_days(2, holi)
        self.assertEqual(target_a, a)
        target_b = BusinessDate.from_ymd(2016, 1, 5)
        b = d.add_business_days(2)  # default holidays contains the target days, i.e. the 1.1.2016
        self.assertEqual(target_b, b)

    def test_from_businesperiod_str(self):
        self.assertEqual(BusinessDate()+ '1B', BusinessDate('1B'))
        self.assertEqual(BusinessDate()+ '1w', BusinessDate('1w'))
        self.assertEqual(BusinessDate().adjust_mod_follow(),
                         BusinessDate('0BMODFLW'))
        self.assertEqual(BusinessDate('20171231').adjust_mod_follow(),
                         BusinessDate('0BMODFLW20171231'))
        self.assertEqual(BusinessDate('20171231').adjust_mod_follow() + '3D',
                         BusinessDate('0B3DMODFOLLOW20171231'))
        self.assertRaises(ValueError, BusinessDate, '0X3D')
        self.assertEqual((BusinessDate('20171231').adjust_mod_follow() + '3D').adjust_mod_follow(),
                         BusinessDate('0B3D0BMODFOLLOW20171231'))
        self.assertEqual(BusinessDate('20171231') + '1w', BusinessDate('1w20171231'))
        self.assertEqual((BusinessDate('20171231').adjust_previous() + '3D').adjust_previous(),
                         BusinessDate('0B3D0BPREV20171231'))
        self.assertEqual((BusinessDate('20171231').adjust_previous() + '3D').adjust_previous(),
                         BusinessDate('0B3D0BPREVIOUS20171231'))
        self.assertEqual((BusinessDate('20171231').adjust_mod_follow() + '3D').adjust_mod_follow(),
                         BusinessDate('0B3D0BMODFOLLOW20171231'))
        self.assertEqual((BusinessDate('20171231').adjust_mod_follow() + '3D').adjust_mod_follow(),
                         BusinessDate('0B3D0BMODFLW20171231'))


class BusinessPeriodUnitTests(unittest.TestCase):
    def setUp(self):
        self._1y = BusinessPeriod('1y')
        self._3m = BusinessPeriod('3m')
        self._1y6m = BusinessPeriod('1y6m')
        self._1b = BusinessPeriod('1b')
        self._2y = BusinessPeriod('2y')
        self._3y = BusinessPeriod('3y')
        self._5y = BusinessPeriod('5y')
        self._2q = BusinessPeriod('2q')
        self._2w = BusinessPeriod('2w')

    def test_constructors(self):
        self.assertEqual(self._1y, BusinessPeriod(years=1))
        self.assertEqual(self._1y6m, BusinessPeriod(years=1, months=6))
        #self.assertEqual(self._1y6m, BusinessPeriod('6m', years=1))
        self.assertEqual(self._1y6m, BusinessPeriod('18m'))
        #self.assertEqual(-1 * self._1y6m, BusinessPeriod('-6m', years=-1))
        self.assertEqual(self._2q, BusinessPeriod(months=6))
        self.assertEqual(BusinessPeriod('-1M'), BusinessPeriod(months=-1))
        self.assertEqual(BusinessPeriod('-12M'), BusinessPeriod(years=-1))
        self.assertEqual(BusinessPeriod('-18M'), BusinessPeriod(years=-1, months=-6))
        self.assertEqual(BusinessPeriod(months=-18), BusinessPeriod(years=-1, months=-6))

        self.assertRaises(ValueError, BusinessPeriod, '6m', years=1)
        self.assertRaises(ValueError, BusinessPeriod, 'XSDW')
        self.assertRaises(ValueError, BusinessPeriod, '2DW')
        self.assertRaises(ValueError, BusinessPeriod, '2B2D')

    def test_properties(self):
        self.assertEqual(self._1y.years, 1)
        self.assertEqual(self._1y.months, 0)
        self.assertEqual(self._1y.days, 0)
        self.assertEqual(-1 * self._1y.years, -1)
        self.assertEqual(-1 * self._1y.days, 0)
        self.assertEqual(self._1b.businessdays, 1)

    def test_operators(self):
        self.assertNotEqual(BusinessPeriod("3M"), BusinessPeriod("1M"))
        self.assertNotEqual(BusinessPeriod("31D"), BusinessPeriod("1M"))
        self.assertEqual(BusinessPeriod("3M"), BusinessPeriod("1M") + "2m")
        self.assertEqual(BusinessPeriod("1Y"), BusinessPeriod("12M"))
        self.assertEqual(BusinessPeriod("1Y"), BusinessPeriod("12M0D"))
        self.assertTrue(self._2y < BusinessPeriod('10Y'))
        self.assertTrue(self._2y < BusinessPeriod('1m') * 12 * 2 + '1d')
        self.assertFalse(self._3y < BusinessPeriod('1Y'))
        self.assertEqual(self._2y.__cmp__(BusinessPeriod('10Y')), -2976.0)
        self.assertNotEqual(self._2y, self._5y)
        self.assertEqual(BusinessPeriod('5y'), self._5y)

    def test_validations(self):
        self.assertTrue(BusinessPeriod.is_businessperiod('1y'))
        self.assertTrue(BusinessPeriod.is_businessperiod('-1y'))
        self.assertTrue(BusinessPeriod.is_businessperiod('1y-6m'))
        self.assertTrue(BusinessPeriod.is_businessperiod('-2b1y6m'))
        self.assertTrue(BusinessPeriod.is_businessperiod('-2b-1y6m'))
        self.assertTrue(BusinessPeriod.is_businessperiod('-2b-1y6m-2b'))

    def test_calculations(self):
        self.assertEqual(self._2y + self._3y, self._5y)
        self.assertEqual(self._1y + '6m', self._1y6m)
        self.assertEqual(self._1y, BusinessPeriod('1y'))
        self.assertRaises(TypeError, lambda: '6m' + self._1y)
        self.assertEquals(self._1y, self._3y - self._2y)
        self.assertEquals(self._1y, self._3y - '2y')

    def test_cast(self):
        self.assertEqual(BusinessPeriod('1y'), BusinessPeriod(years=1))
        self.assertEqual(BusinessDate(20150101) + self._1y, BusinessDate(20160101))
        self.assertEqual(BusinessDate(20150101) + self._1y6m, BusinessDate(20160701))
        self.assertEqual(BusinessDate(20160229) + self._1y, BusinessDate(20170228))

        self.assertEqual((BusinessDate(20160229) + self._1y).to_date(), date(2017, 2, 28))
        self.assertEqual(BusinessDate(20160229) + self._1y - BusinessDate(20160229), self._1y)

        self.assertEqual(str(self._1y), '1Y')
        self.assertEqual(str(self._2q), '6M')
        self.assertEqual(str(self._2w), '14D')
        self.assertEqual(str(BusinessPeriod('-1y6m')), '-1Y6M')
        self.assertEqual(str(BusinessPeriod('1y6m')), '1Y6M')
        self.assertEqual(str(BusinessPeriod('16m')), '1Y4M')

        self.assertEqual(repr(self._2w), "BusinessPeriod('14D')")
        self.assertEqual(self._1y, eval(repr(self._1y)))


class BusinessRangeUnitTests(unittest.TestCase):
    def setUp(self):
        self.sd = BusinessDate(20151231)
        self.ed = BusinessDate(20201231)

    def test_constructors(self):
        br = BusinessRange(self.sd, self.ed)
        self.assertEqual(len(br), 5)
        self.assertEqual(br[0], self.sd)
        self.assertEqual(br[-1], BusinessDate.add_years(self.ed, -1))

        br = BusinessRange(self.sd, self.ed)
        b2 = BusinessRange(self.sd, self.ed, '1y', self.ed)
        ck = BusinessRange(self.sd, self.ed, '1y', self.sd)
        ex = BusinessRange(self.sd, self.ed, '1y', self.ed + '1y')
        sx = BusinessRange(self.sd, self.ed, '1y', self.sd - '1y')
        self.assertEqual(br, b2)
        self.assertEqual(b2, ck)
        self.assertEqual(ck, ex)
        self.assertEqual(ex, sx)

        bs = BusinessRange(20151231, 20160630, '1M', 20151231)
        ck = BusinessDate([20151231, 20160131, 20160229, 20160331, 20160430, 20160531])
        self.assertEqual(bs, ck)

        bs = BusinessRange(20151231, 20160531, '1M', 20151231)
        ck = BusinessRange(20151231, 20160531, '1M', 20160531)
        self.assertEqual(bs, ck)

        bs = BusinessRange(20151231, 20160531, '1M', 20151231)
        ck = BusinessRange(20151231, 20160531, '-1M', 20151231)
        self.assertEqual(bs, ck)


class BusinessScheduleUnitTests(unittest.TestCase):
    def setUp(self):
        self.sd = BusinessDate(20151231)
        self.ed = BusinessDate(20201231)
        self.pr = BusinessPeriod('1y')

    def test_constructors(self):
        bs = BusinessSchedule(self.sd, self.ed, self.pr)
        ck = BusinessSchedule(self.sd, self.ed, self.pr, self.ed)
        for b, c in zip(bs, ck):
            self.assertEqual(b, BusinessDate(c))
        self.assertEqual(len(bs), 6)
        self.assertEqual(bs[0], self.sd)
        self.assertEqual(bs[-1], self.ed)

        bs = BusinessSchedule(20150331, 20160930, '3M', 20160415)
        ck = BusinessDate([20150331, 20150415, 20150715, 20151015, 20160115, 20160415, 20160715, 20160930])
        self.assertEqual(bs, ck)

        bs.adjust()
        ck = BusinessDate([20150331, 20150415, 20150715, 20151015, 20160115, 20160415, 20160715, 20160930])
        self.assertEqual(bs, ck)

        bs = BusinessSchedule(20150101, 20170101, '3M', 20170101)
        ck = BusinessDate([20150101, 20150401, 20150701, 20151001, 20160101, 20160401, 20160701, 20161001, 20170101])
        self.assertEqual(bs, ck)

        bs = BusinessSchedule(20151231, 20160630, '1M', 20151231)
        ck = BusinessDate([20151231, 20160131, 20160229, 20160331, 20160430, 20160531, 20160630])
        self.assertEqual(bs, ck)

        bs = BusinessSchedule(20151231, 20160630, '1M', 20151231)
        ck = BusinessSchedule(20151231, 20160630, '-1M', 20151231)
        self.assertEqual(bs, ck)

        bs = BusinessSchedule(20151231, 20160630, '1M', 20151231)
        ck = BusinessSchedule(20151231, 20160630, '-1M', 20160331)
        self.assertEqual(bs, ck)

    def test_methods(self):
        bs = BusinessSchedule(20150331, 20160930, '3M', 20160415).first_stub_long()
        ck = BusinessDate([20150331, 20150715, 20151015, 20160115, 20160415, 20160715, 20160930])
        self.assertEqual(bs, ck)

        bs.last_stub_long()
        ck = BusinessDate([20150331, 20150715, 20151015, 20160115, 20160415, 20160930])
        self.assertEqual(bs, ck)


class BusinessHolidayUnitTests(unittest.TestCase):
    def setUp(self):
        self.bd = BusinessDate(19730226)
        self.list = [str(i) + '0301' for i in range(1973, 2016)]

    def test_holiday(self):
        h = BusinessHolidays(self.list)
        for l in self.list:
            self.assertTrue(BusinessDate(l).to_date() in h)
        self.assertNotEqual(self.bd.add_period('3b', h), self.bd.add_period('3b'))


class OldDateUnitTests(unittest.TestCase):
    def test__diff(self):
        d1 = BusinessDate.from_ymd(2016, 1, 31)
        d2 = BusinessDate.from_ymd(2017, 11, 1)

        y, m, d = BusinessDate.diff_in_ymd(d2, d1)
        diff = BusinessPeriod(years=y, months=m, days=d)
        self.assertEqual('1Y9M1D', str(diff))

        d1 = BusinessDate.from_ymd(2016, 2, 29)
        d2 = BusinessDate.from_ymd(2017, 3, 1)

        y, m, d = BusinessDate.diff_in_ymd(d2, d1)
        diff = BusinessPeriod(years=y, months=m, days=d)
        self.assertEqual('1Y1D', str(diff))

        d2 = BusinessDate.from_ymd(2017, 2, 28)

        y, m, d = BusinessDate.diff_in_ymd(d2, d1)
        diff = BusinessPeriod(years=y, months=m, days=d)
        self.assertEqual('1Y', str(diff))

        d1 = BusinessDate.from_ymd(2016, 11, 15)
        d2 = BusinessDate.from_ymd(2017, 1, 15)

        y, m, d = BusinessDate.diff_in_ymd(d2, d1)
        diff = BusinessPeriod(years=y, months=m, days=d)
        self.assertEqual('2M', str(diff))

        d1 = BusinessDate.from_ymd(2015, 7, 31)
        d2 = BusinessDate.from_ymd(2017, 2, 20)

        y, m, d = BusinessDate.diff_in_ymd(d2, d1)
        diff = BusinessPeriod(years=y, months=m, days=d)
        self.assertEqual('1Y6M20D', str(diff))


class OldBusinessDateUnitTests(unittest.TestCase):
    """tests the date class """

    def test_type(self):
        s = BusinessDate('20011110')
        e = BusinessDate('20011112')
        self.assertEqual(type(e), type(s))
        self.assertTrue(isinstance(s, BaseDate))

    def test_diff_in_years(self):
        s = BusinessDate('20011110')
        e = BusinessDate('20011112')
        # removed diff_in_years
        # self.assertEqual(BusinessDate.diff_in_years(s, e), 2 / BusinessDate.DAYS_IN_YEAR)
        # self.assertEqual(BusinessDate.diff_in_years(BusinessDate('20161101'),
        #                                             BusinessDate('20171102')), 366 / BusinessDate.DAYS_IN_YEAR)

    def test_diff_in_days(self):
        s = BusinessDate('20011110')
        e = BusinessDate('20011112')
        self.assertEqual(BusinessDate.diff_in_days(s, e), 2)

    def test_add(self):
        s = BusinessDate('20011110')
        e = BusinessDate('20011112')
        self.assertEqual(BusinessDate.add_days(s, e.day), BusinessDate('20011122'))
        self.assertEqual(BusinessDate.add_months(s, 1), BusinessDate('20011210'))
        self.assertEqual(BusinessDate.add_years(s, 1), BusinessDate('20021110'))

    def test_diff(self):
        s = BusinessDate('20160101')
        self.assertEqual(BusinessDate.diff_in_days(s, BusinessDate('20160102')), BusinessPeriod(days=1).days)

    def test_bdc(self):
        self.assertEqual(BusinessDate.adjust_mod_follow(BusinessDate('20160312')), BusinessDate('20160314'))
        self.assertEqual(BusinessDate.is_business_day(BusinessDate('20160312')), False)

    def test_dcc(self):
        self.assertEqual(BusinessDate.get_act_36525(BusinessDate('20170101'),
                                                    BusinessDate('20180101')), 365.0 / 365.25)

    def test_holidays(self):
        self.assertEqual(BusinessDate.is_business_day(BusinessDate('20170101')), False)


class OldBusinessPeriodUnittests(unittest.TestCase):
    def test_add(self):
        p = BusinessPeriod(years=1, months=2, days=3)
        self.assertRaises(TypeError, lambda: p + 2)
        p = BusinessPeriod(years=1, months=2, days=3)
        self.assertEqual(p + '1M', BusinessPeriod(years=1, months=3, days=3))
        self.assertEqual(p + '10Y', BusinessPeriod(years=11, months=2, days=3))

    def test_to_date(self):
        p = BusinessPeriod(years=1, months=2, days=3)
        self.assertEqual(BusinessDate('20160101') + p, BusinessDate('20170304'))

    def test_wrapper_methods(self):
        p = BusinessPeriod(years=1, months=1, days=1)
        self.assertEqual(p + '%sY' %(p.years) + '%sM' %(p.months) + '%sD' %(p.days),
                         BusinessPeriod(years=2, months=2, days=2))
        self.assertEqual(p * 4, BusinessPeriod(years=4, months=4, days=4))
        self.assertEqual(BusinessDate('20160110').add_period(BusinessPeriod(days=-1)),BusinessDate('20160109'))
        self.assertEqual(BusinessDate('20160110') + BusinessPeriod(days=-1),BusinessDate('20160109'))


if __name__ == "__main__":
    import sys

    start_time = datetime.now()

    print('')
    print('======================================================================')
    print('')
    print('run %s' % __file__)
    print('in %s' % os.getcwd())
    print('started  at %s' % str(start_time))
    print('')
    print('----------------------------------------------------------------------')
    print('')

    suite = unittest.TestLoader().loadTestsFromModule(__import__("__main__"))
    testrunner = unittest.TextTestRunner(stream=sys.stdout, descriptions=2, verbosity=2)
    testrunner.run(suite)

    print('')
    print('======================================================================')
    print('')
    print('ran %s' % __file__)
    print('in %s' % os.getcwd())
    print('started  at %s' % str(start_time))
    print('finished at %s' % str(datetime.now()))
    print('')
    print('----------------------------------------------------------------------')
    print('')
