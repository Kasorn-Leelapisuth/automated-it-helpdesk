# Import pandas to work with data tables easily
import pandas as pd
# Import Streamlit for building the web dashboard
import streamlit as st
# Import database functions from our ticket_manager file
from ticket_manager import (
    create_ticket,
    get_all_tickets,
    init_db,
    update_status,
)

# Make sure our database is ready
init_db()

# Configure the browser tab
st.set_page_config(
    page_title="Internal IT Helpdesk", layout="wide", page_icon="🖥️"
)

st.title("Internal IT Support & Incident Portal")

# --- SIDEBAR: Submit New Ticket ---
with st.sidebar:
    st.header("Submit Support Ticket")

    title = st.text_input("Issue Summary")
    category = st.selectbox(
        "Category",
        ["Network", "Hardware", "Software", "Access/Security", "Other"],
    )
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])

    if st.button("Submit Ticket", use_container_width=True):
        if title.strip():
            create_ticket(title, category, priority, source="Employee Portal")
            st.success("Ticket submitted successfully!")
            st.rerun()
        else:
            st.warning("Please provide an issue summary.")

# --- MAIN AREA: Ticket Management ---
tickets = get_all_tickets()

if tickets:
    # Convert database rows into a clean DataFrame table
    df = pd.DataFrame(
        tickets,
        columns=[
            "ID",
            "Title",
            "Category",
            "Priority",
            "Status",
            "Source",
            "Created At",
        ],
    )

    # Show top summary numbers
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", len(df))
    col2.metric("Open", len(df[df["Status"] == "Open"]))
    col3.metric("In Progress", len(df[df["Status"] == "In Progress"]))
    col4.metric(
        "Critical / High", len(df[df["Priority"].isin(["Critical", "High"])])
    )

    st.markdown("---")

    # Filters row: Search bar + Status dropdown filter
    filter_col1, filter_col2 = st.columns([2, 1])

    with filter_col1:
        # Search bar to filter by words in the title
        search_query = st.text_input(
            "🔍 Search tickets by keyword", ""
        ).strip()

    with filter_col2:
        # Filter dropdown to show only tickets with specific status
        status_filter = st.selectbox(
            "Filter by Status", ["All", "Open", "In Progress", "Resolved"]
        )

    # Apply search filter if user typed something
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Title"].str.contains(search_query, case=False)
        ]

    # Apply status filter if user selected anything other than 'All'
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]

    st.subheader(f"Ticket Queue ({len(filtered_df)} shown)")

    # If no tickets match the filter criteria
    if filtered_df.empty:
        st.info("No tickets match your filter criteria.")
    else:
        # Loop over filtered tickets and show them
        for _, row in filtered_df.iterrows():
            with st.expander(
                f"#{row['ID']} - {row['Title']} [{row['Priority']}]"
            ):
                st.write(
                    f"**Category:** {row['Category']} | **Source:** {row['Source']} | **Created:** {row['Created At']}"
                )

                current_status = row["Status"]
                status_options = ["Open", "In Progress", "Resolved"]

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(current_status)
                    if current_status in status_options
                    else 0,
                    key=f"status_{row['ID']}",
                )

                # Save new status if changed
                if new_status != current_status:
                    update_status(row["ID"], new_status)
                    st.rerun()
else:
    st.info("No tickets logged yet.")