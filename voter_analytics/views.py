"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-04-2
Description: Defines Profile and StatusMessage Model
"""
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from . models import Voter
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

class VoterListView(ListView):
    '''View to display voter information'''
    model = Voter
    template_name = "voter_analytics/voters.html"
    paginate_by = 25
    context_object_name = "voters"

    def get_context_data(self, **kwargs):
        '''Add additional context variables'''
        context = super().get_context_data(**kwargs)
        context['time'] = time.ctime()
        return context




    def get_queryset(self):
        '''filter voter data based on any combination of criteria'''
        base_queryset = super().get_queryset()

        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v23town = self.request.GET.get('v23town')

        queryset = base_queryset

        # Apply filters only if they are provided (not empty)
        if party:
            # Add space to match 2-character width format in database
            party_padded = f"{party:<2}"  # Left-align and pad to 2 chars with space
            queryset = queryset.filter(party_affiliation=party_padded)

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))

        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))

        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        # Boolean filters - only apply if checkbox is checked
        if v20state:
            queryset = queryset.filter(v20state='TRUE')

        if v21town:
            queryset = queryset.filter(v21town='TRUE')

        if v21primary:
            queryset = queryset.filter(v21primary='TRUE')

        if v23town:
            queryset = queryset.filter(v23town='TRUE')

        return queryset.order_by('last_name', 'first_name')  # Add ordering to avoid pagination warning

class SingleVoterView(DetailView):
    '''View to display a single voter'''
    model = Voter
    template_name = "voter_analytics/voter.html"
    context_object_name = "voter"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Redirect to the voters list page with an error message
            return redirect(reverse('voters'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = time.ctime()  # Add time to context
        return context

class GraphListView(ListView):
    '''View to display voter information'''
    model = Voter
    template_name = "voter_analytics/graph.html"

    def get_queryset(self):
        '''Reuse filtering logic from VoterListView'''
        base_queryset = super().get_queryset()

        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v23town = self.request.GET.get('v23town')

        queryset = base_queryset

        # Apply filters only if they are provided
        if party:
            party_padded = f"{party:<2}"
            queryset = queryset.filter(party_affiliation=party_padded)

        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))

        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))

        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))

        if v20state:
            queryset = queryset.filter(v20state='TRUE')

        if v21town:
            queryset = queryset.filter(v21town='TRUE')

        if v21primary:
            queryset = queryset.filter(v21primary='TRUE')

        if v23town:
            queryset = queryset.filter(v23town='TRUE')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use filtered queryset instead of all voters
        filtered_voters = self.get_queryset()

        # Create subplot with 3 rows and 1 column
        fig = make_subplots(
            rows=3, cols=1,
            specs=[[{"type": "histogram"}], [{"type": "pie"}], [{"type": "bar"}]],
            subplot_titles=("Distribution by Birth Year",
                          "Distribution by Party",
                          "Voter Participation by Election"),
            vertical_spacing=0.3,
            row_heights=[0.3, 0.35, 0.35]
        )

        # Get birth years data from filtered queryset
        voters = list(filtered_voters.values_list('date_of_birth', flat=True))
        birth_years = [d.year for d in voters]

        # Count frequency of each birth year
        year_counts = {}
        for year in birth_years:
            year_counts[year] = year_counts.get(year, 0) + 1

        # Sort years for proper x-axis ordering
        sorted_years = sorted(year_counts.keys())
        year_frequencies = [year_counts[year] for year in sorted_years]

        # Get party affiliation data from filtered queryset
        party_dict = {}
        for voter in filtered_voters:
            party = voter.party_affiliation.strip()
            if party in party_dict:
                party_dict[party] += 1
            else:
                party_dict[party] = 1

        parties = []
        counts = []
        party_labels = {
            'U': 'U',
            'D': 'D',
            'R': 'R',
            'CC': 'CC',
            'L': 'L',
            'J': 'J',
            'T': 'T',
            'O': 'O',
            'A': 'A',
            'Q': 'Q',
            'S': 'S',
            'G': 'G',
            'X': 'X',
            'AA': 'AA',
            'Z': 'Z',
            'FF': 'FF',
            'GG': 'GG',
            'V': 'V',
            'K': 'K',
            'HH': 'HH',
            'P': 'P',
            'E': 'E',
            'H': 'H',
            'Y': 'Y',
            'W': 'W',
            'EE': 'EE',
            '': 'No Party'
        }

        for party, count in party_dict.items():
            label = party_labels.get(party, party)  # Just use the code itself
            parties.append(label)
            counts.append(count)

        # Get election participation data from filtered queryset
        election_data = {
            '2020 State': sum(1 for v in filtered_voters if v.v20state == 'TRUE'),
            '2021 Town': sum(1 for v in filtered_voters if v.v21town == 'TRUE'),
            '2021 Primary': sum(1 for v in filtered_voters if v.v21primary == 'TRUE'),
            '2022 General': sum(1 for v in filtered_voters if v.v22general == 'TRUE'),
            '2023 Town': sum(1 for v in filtered_voters if v.v23town == 'TRUE')
        }

        # Add histogram for birth years (as a bar chart for exact year counts)
        fig.add_trace(
            go.Bar(
                x=sorted_years,
                y=year_frequencies,
                name='Voters',
                showlegend=False
            ),
            row=1, col=1
        )

        # Add pie chart for party distribution
        fig.add_trace(
            go.Pie(labels=parties, values=counts, name='Party Distribution'),
            row=2, col=1
        )

        # Add bar chart for election participation
        fig.add_trace(
            go.Bar(
                x=list(election_data.keys()),
                y=list(election_data.values()),
                name='Voter Participation',
                showlegend=False
            ),
            row=3, col=1
        )

        # Update layout
        fig.update_layout(
            height=1800,  # Increased height for third plot
            width=1200,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                color='rgb(117, 88, 93)'
            ),
            legend=dict(
                yanchor="middle",
                y=0.55,  # Adjusted to align with raised pie chart
                xanchor="right",
                x=1.2
            ),
            # Add margin adjustment to fine-tune positioning
            margin=dict(t=100, b=100)
        )

        # Update x-axis to show all years with spacing
        fig.update_xaxes(
            title_text="Birth Year",
            gridcolor='rgba(255,192,203,0.2)',
            zerolinecolor='rgba(255,192,203,0.4)',
            dtick=2,  # Show every other year
            tickangle=45,  # Angle the year labels for better readability
            tickmode='linear',
            row=1, col=1
        )

        # Update layout to accommodate angled labels
        fig.update_layout(
            height=1800,  # Increased height for third plot
            width=1200,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                color='rgb(117, 88, 93)'
            ),
            legend=dict(
                yanchor="middle",
                y=0.55,
                xanchor="right",
                x=1.2
            ),
            margin=dict(
                t=100,  # top margin
                b=150,  # increased bottom margin for angled labels
                l=100,  # left margin
                r=100   # right margin
            )
        )
        fig.update_yaxes(
            title_text="Number of Voters",
            gridcolor='rgba(255,192,203,0.2)',
            zerolinecolor='rgba(255,192,203,0.4)',
            row=1, col=1
        )

        # Update axes for election participation bar chart
        fig.update_xaxes(
            title_text="Election",
            gridcolor='rgba(255,192,203,0.2)',
            zerolinecolor='rgba(255,192,203,0.4)',
            row=3, col=1
        )
        fig.update_yaxes(
            title_text="Number of Voters",
            gridcolor='rgba(255,192,203,0.2)',
            zerolinecolor='rgba(255,192,203,0.4)',
            row=3, col=1
        )

        # Convert figure to HTML
        graph_div = fig.to_html(
            full_html=False,
            include_plotlyjs=True
        )

        context['graph_div'] = graph_div
        context['time'] = time.ctime()
        return context
