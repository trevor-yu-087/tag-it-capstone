import model
import view


class Controller:

    def __init__(self, view, model):

        self.view = view
        self.model = model
        self.connect_signals()

        # when we go to a patient's report screen:
        self.initial_reports_display()



    def connect_signals(self):
        """Connect signals and slots."""
        self.view.import_button.clicked.connect(self.import_file)
        self.view.filter_button.clicked.connect(self.filter_selection)
        self.view.dialog_button.clicked.connect(self.apply_filters)
        self.view.report_table.cellPressed.connect(self.view_report)
        self.view.go_button.clicked.connect(self.begin_search)
        self.view.clear_filters_button.clicked.connect(self.clear_filters)
        self.view.dialog_clear_filters_button.clicked.connect(self.clear_dialog_filters)
        self.view.remove_filter_buttons.buttonClicked.connect(self.remove_one_filter)

    def view_report(self, row, col):
        filename, isPDF, name = self.model.view_report(row, col)
        if isPDF:
            self.view.display_pdf(filename, name, row, col)
        else:
             self.view.display_image_report(filename, name)

    def begin_search(self):
        user_query = self.view.search_bar.text()
        report_IDs = self.model.search(user_query)
        self.get_report_info_to_display(report_IDs)
        self.display_report_info()


    def import_file(self):
        self.view.show_directory()
        if self.view.explorer:
            self.file_selection = self.view.explorer
            self.view.import_enabled(False)
            # start a thread
            import_file_thread = self.view.create_thread(self)
            import_file_thread.finished.connect(self.display_report_info)
            import_file_thread.start()

    def thread_interior(self):
        self.model.import_report(self.file_selection)
        self.get_report_info_to_display()
       # self.view.worker.worker_finished()

    def filter_selection(self):
        self.view.show_dialog()

    def apply_filters(self):
        active_filters = self.model.set_filters(self.view.mod_options, self.view.bodypart_options, self.view.date_options)
        self.populate_filter_layout(active_filters)
        self.get_filtered_reports()
        self.view.close_dialog()

    def populate_filter_layout(self, active_filters):
        self.model.clear_filters_layout(self.view.filters_layout)
        if len(active_filters) != 0:
            self.view.populate_filters_layout(active_filters)

    def get_filtered_reports(self):
        report_IDs = self.model.get_filtered_ids()
        self.get_report_info_to_display(report_IDs)
        self.display_report_info()

    def clear_filters(self):
        self.model.clear_filters_layout(self.view.filters_layout)
        self.model.reset_current_filters()
        self.model.reset_filter_checkboxes([self.view.mod_options, self.view.bodypart_options, self.view.date_options])
        self.initial_reports_display()

    def clear_dialog_filters(self):
        self.model.reset_filter_checkboxes([self.view.mod_options, self.view.bodypart_options, self.view.date_options])

    def remove_one_filter(self, filter_to_remove):
        self.model.uncheck_filter(filter_to_remove, [self.view.mod_options, self.view.bodypart_options, self.view.date_options])
        self.apply_filters()

    def initial_reports_display(self):
        self.get_report_info_to_display()
        self.display_report_info()

    def get_report_info_to_display(self, ids=None):
        self.reports = self.model.get_reports_to_display(ids)
        self.rows = len(self.reports)


    def display_report_info(self):
        self.view.set_table_row_count(self.rows)
        self.view.populate_report_table(self.reports)
        self.view.import_enabled(True)