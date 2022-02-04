import model
import view


class Controller:

    def __init__(self, view, model):

        self.view = view
        self.model = model
        self.create_table_grid()
        self.create_settings_dialog()
        self.connect_signals()


        # when we go to a patient's report screen:
        self.initial_reports_display()



    def connect_signals(self):
        """Connect signals and slots."""
        self.view.report_screen.import_button.clicked.connect(self.import_file)
        self.view.report_screen.filter_button.clicked.connect(self.filter_selection)
        self.view.report_screen.dialog_button.clicked.connect(self.apply_filters)
        self.view.report_screen.report_table.cellPressed.connect(self.view_report)
        self.view.report_screen.go_button.clicked.connect(self.begin_search)
        self.view.report_screen.search_bar.returnPressed.connect(self.begin_search)
        self.view.report_screen.clear_filters_button.clicked.connect(self.clear_filters)
        self.view.report_screen.dialog_clear_filters_button.clicked.connect(self.clear_dialog_filters)
        self.view.report_screen.remove_filter_buttons.buttonClicked.connect(self.remove_one_filter)
        self.view.report_screen.settings_button.clicked.connect(self.select_settings)
        self.view.report_screen.apply_settings_button.clicked.connect(self.apply_settings)
        self.view.report_screen.back_button.clicked.connect(self.patient_select_screen)
        self.view.report_screen.main_menu_button.clicked.connect(self.view.go_to_home)

        self.view.home.select_button.clicked.connect(self.patient_select_screen)
        self.view.home.quit_button.clicked.connect(self.view.close)

        self.view.patient_select.back_button.clicked.connect(self.view.go_to_home)
        self.view.patient_select.patient_table.cellPressed.connect(self.view_patient)


    def patient_select_screen(self):
        self.view.go_to_patient_select()
        patient_data = self.model.get_patient_data()
        self.view.patient_select.populate_table(patient_data)

    def view_patient(self, row, col):
        patient = self.view.patient_select.patient_table.item(row, 0).text()
        self.model.set_current_patient_ID(int(patient))
        self.get_report_info_to_display()
        self.display_report_info()
        self.view.report_screen.set_patient_name(self.model.get_patient_name())
        self.view.go_to_report_screen()


    def view_report(self, row, col):
        filename, isPDF, name = self.model.view_report(row, col)
        if isPDF:
            self.view.report_screen.display_pdf(filename, name, row, col)
        else:
             self.view.report_screen.display_image_report(filename, name)

    def begin_search(self):
        user_query = self.view.report_screen.search_bar.text()
        report_IDs = self.model.search(user_query)
        self.get_report_info_to_display(report_IDs)
        self.display_report_info()

    def import_file(self):
        self.view.report_screen.show_directory()
        if self.view.report_screen.explorer:
            self.file_selection = self.view.report_screen.explorer
            self.view.report_screen.import_enabled(False)
            # start a thread
            import_file_thread = self.view.report_screen.create_thread(self)
            import_file_thread.finished.connect(self.display_report_info)
            import_file_thread.start()

    def thread_interior(self):
        self.model.import_report(self.file_selection)
        self.get_report_info_to_display()

    def filter_selection(self):
        self.view.report_screen.show_dialog()

    def apply_filters(self):
        active_filters = self.model.set_filters(self.view.report_screen.mod_options,
                                                self.view.report_screen.bodypart_options,
                                                self.view.report_screen.date_options)
        self.populate_filter_layout(active_filters)
        self.get_filtered_reports()
        self.view.report_screen.close_dialog()

    def populate_filter_layout(self, active_filters):
        self.model.clear_layout(self.view.report_screen.filters_layout)
        if len(active_filters) != 0:
            self.view.report_screen.populate_filters_layout(active_filters)

    def get_filtered_reports(self):
        report_IDs = self.model.get_filtered_ids()
        self.get_report_info_to_display(report_IDs)
        self.display_report_info()

    def clear_filters(self):
        self.model.clear_layout(self.view.report_screen.filters_layout)
        self.model.reset_current_filters()
        self.model.reset_filter_checkboxes([self.view.report_screen.mod_options,
                                            self.view.report_screen.bodypart_options,
                                            self.view.report_screen.date_options])
        self.initial_reports_display()

    def clear_dialog_filters(self):
        self.model.reset_filter_checkboxes([self.view.report_screen.mod_options,
                                            self.view.report_screen.bodypart_options,
                                            self.view.report_screen.date_options])

    def remove_one_filter(self, filter_to_remove):
        self.model.uncheck_filter(filter_to_remove, [self.view.report_screen.mod_options,
                                                     self.view.report_screen.bodypart_options,
                                                     self.view.report_screen.date_options])
        self.apply_filters()

    def initial_reports_display(self):
        self.get_report_info_to_display()
        self.display_report_info()

    def get_report_info_to_display(self, ids=None):
        self.reports = self.model.get_reports_to_display(ids)
        self.rows = len(self.reports)

    def display_report_info(self):
        self.view.set_table_row_count(self.rows, self.view.report_screen.report_table)
        self.view.report_screen.populate_report_table(self.reports)
        self.view.report_screen.import_enabled(True)

    def create_table_grid(self):
        current_categories = self.model.current_categories
        self.view.report_screen.create_table_grid(current_categories)

    def select_settings(self):
        self.view.report_screen.show_settings_dialog()

    def apply_settings(self):
        # determine which checkboxes are checked
        self.model.determine_checked_categories(self.view.report_screen.category_list)
        self.view.report_screen.create_table_columns(self.model.current_categories)
        self.get_report_info_to_display(self.model.current_report_IDs)
        self.display_report_info()
        self.view.report_screen.close_settings_dialog()

    def create_settings_dialog(self):
        self.view.report_screen.create_categories()
        self.model.update_view_category_list(self.view.report_screen.category_list)
        self.view.report_screen.create_settings_dialog_for_later()