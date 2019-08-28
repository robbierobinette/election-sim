import plotly.graph_objects as go
import plotly
import pandas as pd
import numpy as np

z_df = pd.read_csv('HSall_members.csv')
z_np = z_df.values

n_buckets = 20
rows = 116
cols = n_buckets * 2 + 1
hd_raw = {}
next_party_id = 0
count_for_session = np.zeros([rows])

for r in range(np.shape(z_np)[0]):
    if z_np[r, 1] == 'House':
        try:
            party_id = z_np[r, 6]
            session = z_np[r, 0] - 1
            n_d1 = -z_np[r, 13]
            n_index = int(round(n_d1 * n_buckets)) + n_buckets
            if party_id not in hd_raw:
                hd_raw[party_id] = np.zeros([rows, cols])
            hd_raw[party_id][session, n_index] += 1
            count_for_session[session] += 1
        except Exception:
            print("can't parse line:  ", z_df.iloc[r])


def build_smooth_surface(z_data, sr, sc):
    smooth_data = np.zeros_like(z_data)
    for r in range(rows):
        for c in range(np.shape(z_data)[1]):
            rmn = max(0, r - sr)
            rmx = min(rows - 1, r + sr + 1)
            cmn = max(0, c - sc)
            cmx = min(cols - 1, c + sc + 1)
            z_sum = np.sum(z_data[rmn: rmx, cmn: cmx])
            count = (rmx - rmn + 1) * (cmx - cmn + 1)
            smooth_data[r, c] = z_sum / count

    for r in range(np.shape(smooth_data)[0]):
        smooth_data[r] /= count_for_session[r]

    return smooth_data


y_data = np.array(range(1, rows)) * 2 + 1787
x_data = (np.array(range(0, cols)) - n_buckets) / n_buckets

y_data = y_data[-30:]


reds = build_smooth_surface(hd_raw[200], 0, 3)[-30:]
blues = build_smooth_surface(hd_raw[100], 0, 3)[-30:]

surfaces = [
    go.Surface(z = reds, x = x_data, y = y_data, colorscale = "Reds", name = "Republicans"),
    go.Surface(z = blues, x = x_data, y = y_data, colorscale = "Blues", name = "Democrats")
]
fig = go.Figure(layout_title_text = "Congressional Ideology 1960 to 2017 split by party",  data = surfaces)
plotly.io.write_html(fig, "ideology_by_party.html")
fig.show()

z_combined = reds + blues
surface_2 = [
    go.Surface(z = z_combined, x = x_data, y = y_data, name = "Representatives")
]
fig2 = go.Figure(layout_title_text = "Congressional Ideology, Combined", data = surface_2)
fig2.show()
plotly.io.write_html(fig2, "combined_ideology.html")

# fig = go.Figure(data = [go.Surface(z = smooth_data, x = x_data, y = y_data)])
# fig.show()

#
# f2_rows = 40
# print(np.shape(smooth_data))
# print(np.shape(smooth_data[-f2_rows:]))
# l = smooth_data[-f2_rows:]
# y2 = y_data[-f2_rows:]
#
# fig2 = go.Figure(data = [go.Surface(z = l, x = x_data, y = y2)])
# plotly.io.write_html(fig2, "fig2.html")
# fig2.show()
# fig2.save("fig2")
