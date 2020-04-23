import networkx as nx
from networkx.algorithms.flow.maxflow import maximum_flow
import matplotlib.pyplot as plt


class NodalMarket():
    def __init__(self):
        self.G = nx.DiGraph()
        self.transmission = {}
        self.surplus_gen_capacity = {}

    def add_node(self, node_label):
        """
        Adds a trading node (ie location in a locational marginal pricing market).
        """
        self.G.add_node(node_label)
    
    def set_transmission(self, from_node, to_node, capacity, label):
        """
            Adds unidirectional transmission between two nodes, at a certain capacity (MW)
            Label must be unique. 
        """
        key = from_node+'-'+to_node
        self.transmission[key] = {} if key not in self.transmission else self.transmission[key]
        self.transmission[key][label] = {'from_node':from_node, 'to_node': to_node, 'label':label, 'capacity':int(capacity)}
        total = sum([self.transmission[key][label]['capacity'] for label in self.transmission[key] ])
        self.G.add_edge(from_node,to_node,capacity=int(total))
    
    def set_surplus_capacity(self, node, gen_capacity):
        """
            Set surplus generation capacity on a given node. 
        """
        self.surplus_gen_capacity[node] = gen_capacity
    
    def clear_surplus_capacity(self):
        """
            Clears/resets all surplus generation capacity at all nodes. 
        """
        self.surplus_gen_capacity = {}

    def get_transmission(self):
        return self.transmission

    def calculate_max_flow(self, to_node):
        # Add a consolidated source node to all nodes with spare capacities. 
        self.G.add_node('Consolidated Source')
        for node in self.surplus_gen_capacity:
            self.G.add_edge('Consolidated Source', node, capacity=int(self.surplus_gen_capacity[node]))
        
        flow_value, flow_dict = maximum_flow(self.G, 'Consolidated Source', to_node)

        # Cleaning Up - Remove the consolidated source node.
        self.G.remove_node('Consolidated Source')
        return flow_value
        
    def print(self):
        print("Edges:")
        for e in self.G.edges:
            print(e, self.G.edges[e])
        

    def draw(self):
        
        nx.draw(self.G)
        plt.show()

class LMPFactory():
    def get_australian_nem(self, date_time):
        market = NodalMarket()
        market.add_node('NSW')
        market.add_node('VIC')
        market.add_node('SA')
        market.add_node('QLD')
        market.add_node('TAS')

        search = INTERCONNECTORRES.objects(SETTLEMENTDATE=date_time).fields(INTERCONNECTORID=1, EXPORTLIMIT=1, IMPORTLIMIT=1)
        result = {d.INTERCONNECTORID: d for d in search}

        # Now there is a bit of a mystery around what the numbers on export and import limits mean. 
        # I think its a range, where export limit is always > import limit. 
        # ie. the Terranora code is N-Q-MNSP1
        # So its NSW-QLD
        # So when positive, flowing NSW-QLD
        # When negative, flowing QLD-NSW, 
        # And the export and importlimits set up a range at which flow might occur. 

        market.set_transmission('NSW', 'QLD', max(result['N-Q-MNSP1'].EXPORTLIMIT, 0) if 'N-Q-MNSP1' in result else 107, "Terranora NSW->QLD")
        market.set_transmission('QLD', 'NSW', abs(min(result['N-Q-MNSP1'].IMPORTLIMIT, 0 )) if 'N-Q-MNSP1' in result else 210, "Terranora QLD->NSW")
        market.set_transmission('NSW', 'QLD', max(result['NSW1-QLD1'].EXPORTLIMIT, 0) if 'NSW1-QLD1' in result else 600, "Queensland NSW Interconnector NSW->QLD")
        market.set_transmission('QLD', 'NSW', abs(min(result['NSW1-QLD1'].IMPORTLIMIT, 0 )) if 'NSW1-QLD1' in result else 1078, "Queensland NSW Interconnector QLD->NSW")
        market.set_transmission('VIC', 'NSW', max(result['VIC1-NSW1'].EXPORTLIMIT, 0) if 'VIC1-NSW1' in result else 1600, "Victoria to NSW Interconnector VIC->NSW")
        market.set_transmission('NSW', 'VIC', abs(min(result['VIC1-NSW1'].IMPORTLIMIT, 0 )) if 'VIC1-NSW1' in result else 1350, "Victoria to NSW Interconnector NSW->VIC")
        market.set_transmission('TAS', 'VIC', max(result['T-V-MNSP1'].EXPORTLIMIT, 0) if 'T-V-MNSP1' in result else 594, "Basslink TAS->VIC") 
        market.set_transmission('VIC', 'TAS', abs(min(result['T-V-MNSP1'].IMPORTLIMIT, 0 )) if 'T-V-MNSP1' in result else 478, "Basslink VIC->TAS")
        market.set_transmission('VIC', 'SA', max(result['V-SA'].EXPORTLIMIT, 0) if 'V-SA' in result else 600, "Heywood Interconnector VIC->SA") 
        market.set_transmission('SA', 'VIC', abs(min(result['V-SA'].IMPORTLIMIT, 0 )) if 'V-SA' in result else 500, "Heywood Interconnector SA->VIC")
        market.set_transmission('VIC', 'SA', max(result['V-S-MNSP1'].EXPORTLIMIT, 0) if 'V-S-MNSP1' in result else 220, "Murraylink VIC->SA") 
        market.set_transmission('SA', 'VIC', abs(min(result['V-S-MNSP1'].IMPORTLIMIT, 0 )) if 'V-S-MNSP1' in result else 200, "Murraylink SA->VIC")

        return market

if __name__ == "__main__":
    # Interconnector capacities below taken as maximums in 'INTERCONNECTOR CAPABILITIES FOR THE NATIONAL ELECTRICITY MARKET' (2017) https://www.aemo.com.au/-/media/Files/Electricity/NEM/Security_and_Reliability/Congestion-Information/2017/Interconnector-Capabilities.pdf
    market = LMPFactory().get_australian_nem()
    
    # I think these need to be netted internally - seems to only support one edge between two nodes. 
    flow = market.calculate_flow('SA', {'VIC': 100, 'NSW': 50, 'QLD': 600} )
    print(flow)

    # market.draw()
    market.print()


# Breadth first search. Start with the closest nodes. Calc maximum flow at their max avail. Constrain closest lines as per flow. Repeat. 

# This is NEARLY the maximum flow algorithm with multiple sources and one sink. 
# To do this you add a consolidated source connected to each node, with constraints at the required node residual capacities. 
# YES. Solved. 