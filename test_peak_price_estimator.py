from peak_price_estimator import *

def test_closer_to_winter():
    summer_date = pendulum.datetime(2010,1,1)
    assert not closer_to_winter(summer_date)
    winter_date = pendulum.datetime(2013, 6, 2)
    assert closer_to_winter(winter_date)

def test_generate_demand_curve_from_price_bands():
    cumulative_price_bands = [(300, 500, 10) , (500,1000, 20),  (1000, 7500, 30), (7500, MPC, 40) ,(MPC, MPC, 50)]
    
    # Test with MPC bid, higher demand than flex curve. 
    curve = generate_demand_curve_from_price_bands(cumulative_price_bands, 200)
    expected_curve = [(MPC, 160), (7500, 10), (1000, 10), (500, 10), (300, 10)]
    print("Expected Curve 1: ", expected_curve)
    print("Generated Curve 1: ", curve)
    for i in range(len(curve)):
        assert curve[i] == expected_curve[i]

    # Test with MPC bid, lower demand than flex curve.
    curve = generate_demand_curve_from_price_bands(cumulative_price_bands, 35)
    expected_curve = [(7500, 5), (1000, 10), (500, 10), (300, 10)]
    print("Expected Curve 2: ", expected_curve)
    print("Generated Curve 2: ", curve)
    for i in range(len(curve)):
        assert curve[i] == expected_curve[i]

    # Test with higher demand than flex curve, no MPC bid
    cumulative_price_bands = [(300, 500, 10) , (500,1000, 20),  (1000, 7500, 30), (7500, MPC, 40) ]
    curve = generate_demand_curve_from_price_bands(cumulative_price_bands, 100)
    expected_curve = [(MPC, 60),(7500, 10), (1000, 10), (500, 10), (300, 10)]
    print("Expected Curve 3: ", expected_curve)
    print("Generated Curve 3: ", curve)
    for i in range(len(curve)):
        assert curve[i] == expected_curve[i]
    
     # Test with lower demand than flex curve, no MPC bid
    cumulative_price_bands = [(300, 500, 10) , (500,1000, 20),  (1000, 7500, 30), (7500, MPC, 40) ]
    curve = generate_demand_curve_from_price_bands(cumulative_price_bands, 30)
    expected_curve = [(1000, 10), (500, 10), (300, 10)]
    print("Expected Curve 4: ", expected_curve)
    print("Generated Curve 4: ", curve)
    for i in range(len(curve)):
        assert curve[i] == expected_curve[i]


def test_get_demand_curve():
    curve = get_demand_curve(pendulum.datetime(2050, 1, 1), 5000, 'NSW')
    # original cumulative price bands are [ (300, 500, 564.11),  (500, 1000, 1057.55), (1000, 7500, 1084.05), (7500, MPC, 1267.11) ,(MPC, MPC, 1267.11)],
    expected = [(MPC, 5000 - 1267.11),(7500, 1267.11 - 1084.05 ) ,(1000, 1084.05 - 1057.55),(500, 1057.55 - 564.11 ),(300, 564.11)]
    for i in range(len(curve)):
        assert curve[i] == expected[i]

def test_make_rational_bid_decision():
    # Should bid 1 unit shadowing ceiling price.
    decision = make_rational_bid_decision(50, [(MPC, 50), (100, 30), (50, 19)])
    expected = (MPC-1, 1)
    assert expected == decision

    # Should bid 45 units at 49 dollars.
    decision = make_rational_bid_decision(50, [(70, 1), (60, 4), (50, 45)])
    expected = (50-1, 45)
    assert expected == decision

    # Should bid 40 units at 59 dollars.
    decision = make_rational_bid_decision(50, [(70, 1), (60, 40), (50, 5)])
    expected = (60-1, 40)
    assert expected == decision

    