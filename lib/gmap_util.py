import googlemaps
import gmaps
import pandas as pd
from IPython.display import display
import ipywidgets as widgets
from .base import CLIENT, DEBUG


def get_location(item):
    return (item['LAT'], item['LNG'])


def get_direction(worker, office):
    start = get_location(worker)
    end = get_location(office)
    return Direction(start, end)


class Direction:
    def __init__(self, start, end):
        print(f'get direction from {start} to {end}')
        # TODO: in many cases can't find public routes
        #self.layer = gmaps.directions_layer(start, end, travel_mode='TRANSIT')
        #self.data = CLIENT.directions(start, end, mode='transit')
        self.layer = gmaps.directions_layer(start, end, show_markers=False)
        self.data = CLIENT.directions(start, end)
        assert self.data


class CommutingMap:
    def __init__(self):
        self.base_map = gmaps.figure()
        self.office_df = pd.read_csv('./data/fabbit-location.csv')
        self.worker_df = pd.read_csv('./data/tokyo-worker.csv')
        if DEBUG:
            self.office_df = self.office_df[:2]
            self.worker_df = self.worker_df[:2]

        self.office_layer = gmaps.marker_layer(
            list(zip(self.office_df.LAT, self.office_df.LNG)),
            info_box_content=self.office_df.NAME,
        )
        self.worker_layer = gmaps.symbol_layer(
            list(zip(self.worker_df.LAT, self.worker_df.LNG)),
            fill_color='blue', stroke_color='blue', scale=5,
            info_box_content=self.worker_df.NAME,
        )

        print('setting up directions....')
        self.direction_pair = []

        for _, office in self.office_df.iterrows():
            directions = []
            for _, worker in self.worker_df.iterrows():
                print(f'get direction for {worker.NAME} to {office.NAME}')
                d = get_direction(worker, office)
                directions.append(d)
            self.direction_pair.append(directions)
        print('completed!')

    def get_map_and_time(self, worker_idxs, office_idx):
        fig = gmaps.figure()
        total_min = 0
        time = {}
        directions = self.direction_pair[office_idx]
        for i in worker_idxs:
            d = directions[i]
            fig.add_layer(d.layer)
            dur_sec = d.data[0]['legs'][0]['duration']['value']
            dur_min = dur_sec // 60
            time[self.worker_df.loc[i].NAME] = dur_min
            total_min += dur_sec / 60

        fig.add_layer(self.office_layer)
        fig.add_layer(self.worker_layer)
        return (fig, total_min, time)

    def show_result(self, worker_idxs, office_idx):
        fig, total, time = self.get_map_and_time(worker_idxs, office_idx)
        avg = int(total / len(worker_idxs))
        print(f'Average Commute Time: {avg} min')
        print('=============================')
        for name, m in time.items():
            print(f'{name:20}| {m:3} min')
        print()
        display(fig)

    def create_widgets(self):
        style = {'description_width': 'initial'}
        widgets.interact(
            self.show_result,
            worker_idxs=widgets.SelectMultiple(
                options=[(w.NAME, i) for i, w in self.worker_df.iterrows()],
                value=(0,),
                description='Workers (multiple)',
                style=style,
            ),
            office_idx=widgets.RadioButtons(
                options=[(o.NAME, i) for i, o in self.office_df.iterrows()],
                value=0,
                description='Office',
                style=style,
            ),
        )
