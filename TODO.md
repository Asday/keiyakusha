* [ ] Time tracking
  * [ ] Time entries can be created
    * [ ] Refer to a client
    * [ ] Default start time is the end time of the last entry
      * [ ] Within reason?
    * [ ] Start time can be set to "now" with a button
    * [ ] Times can be entered as a 4 digit number and interpreted sensibly
      * [ ] Do what I _mean_ damnit
  * [x] Can get the currently running time entry from the Manager
  * [ ] Button to sign off the current time entry
  * [ ] Running totals shown
    * [x] Current invoice period
    * [x] Current week
    * [ ] Current "day"
      * [ ] Non-naiive definition of "day", working over the midnight barrier doesn't definitely mean a new day
        * [x] First just have a naiive "day" definition
    * [x] Currently running entry if there is one
  * [ ] Toggl export
* [ ] Invoice generation
  * [ ] Generates a PDF
  * [ ] Keeps track of over-under charging and evens it out over time
    * [ ] Shows current over-under charge amount
    * [ ] Rounds hours on an invoice up or down depending on what will result in the lowest under-overcharge disparity
      * [ ] Favour over-charging?  By what ratio?  It'll never be more than an hour out in any case.
  * Create invoices early and be able to see "invoices in progress"?  Or create invoices on demand?
    * Probably on demand.
* [ ] Account management
  * [ ] Link payments in the real life bank account to invoices sent
* Data/display app separation?
