class Statistics:
    '''
    Runs simulations, collects statistics and generates graphs on a
    given Action with provided conditions

    Inputs:
    Action: The Action to collect statistics on
    d20_success_target: Adjusted (post modifiers) number on the d20 to
    meet or exceed for a success

    nr_d20s: Number of d20s to roll to determine success.
    1 is regular,
    2 is for advantage or disadvantage,
    3 is elven accuracy

    fail_dmg_scale: Damage of a failed Action.
    Attacks usually deal no damage (0.0), but some spells fail for half (0.5)

    dmg_scale: Overall damage scale. Resistance = 0.5, Vulnerability = 2.0

    disadvantage: Whether multiple d20s are rolled with
    advantage or disadvantage
    '''

    def __init__(self, action):
        self.statistics = []

        self.action = action

        self.max_damage = 0
        self.min_damage = 0
        self.avg_damage = 0
        self.percentiles = [0, 0, 0, 0, 0]  # 90, 75, 50, 25, 10

    def reset_statistics(self):
        self.statistics = []

    def plot_histogram(self, alpha=1.0, label='0'):
        # plot = plt.figure()
        plt.hist(
            self.statistics, bins=self.max_damage+1,
            range=[-0.5, self.max_damage+0.5], density=True,
            alpha=alpha, label=label)
        # return plot

    def plot_cumulative(self):
        # plot = plt.figure()
        plt.hist(
            self.statistics, bins=self.max_damage+1,
            range=[-0.5, self.max_damage+0.5],
            cumulative=-1, histtype='step')
        # return plot

    def collect_statistics(self, N=100000, append=False):
        if not append:
            self.reset_statistics()

        for i in range(N):
            self.statistics.append(self.action.perform())

        self.max_damage = max(self.statistics)
        self.min_damage = min(self.statistics)
        self.avg_damage = sum(self.statistics)/len(self.statistics)

        self.statistics.sort()

        self.percentiles[0] = np.percentile(self.statistics, 10)
        self.percentiles[1] = np.percentile(self.statistics, 25)
        self.percentiles[2] = np.percentile(self.statistics, 50)
        self.percentiles[3] = np.percentile(self.statistics, 75)
        self.percentiles[4] = np.percentile(self.statistics, 90)

    def report_statistics(self):
        return {'Min': self.min_damage,
                'Max': self.max_damage,
                'Avg': self.avg_damage,
                'Percentiles': self.percentiles}

if __name__ == '__main__':
    print("hey")
