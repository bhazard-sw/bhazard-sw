local addonName, InventoryRequest = ...

-- Create the main frame for the addon interface
local frame = CreateFrame("Frame", "InventoryRequestFrame", UIParent, "UIPanelDialogTemplate")
frame:SetSize(400, 300)  -- Set the size of the frame
frame:SetPoint("CENTER")  -- Place the frame at the center of the screen
frame:SetMovable(true)  -- Allow the frame to be moved around
frame:EnableMouse(true)  -- Enable mouse interaction
frame:RegisterForDrag("LeftButton")  -- Enable dragging with the left mouse button
frame:SetScript("OnDragStart", frame.StartMoving)  -- Start moving the frame when dragging
frame:SetScript("OnDragStop", frame.StopMovingOrSizing)  -- Stop moving the frame when drag ends
frame:Hide()  -- Initially hide the frame

-- Create a scrollable edit box to display the output (item names and counts)
local scrollFrame = CreateFrame("ScrollFrame", nil, frame, "UIPanelScrollFrameTemplate")
scrollFrame:SetSize(360, 220)  -- Set the size of the scrollable area
scrollFrame:SetPoint("TOP", 0, -30)  -- Position it within the main frame

-- Create the edit box inside the scrollable frame
local editBox = CreateFrame("EditBox", nil, scrollFrame)
editBox:SetMultiLine(true)  -- Allow multiple lines in the edit box
editBox:SetSize(360, 220)  -- Set the size of the edit box
editBox:SetFontObject("ChatFontNormal")  -- Use a normal chat font for display
editBox:SetAutoFocus(false)  -- Prevent auto focus when opened
editBox:SetScript("OnEscapePressed", function(self) self:ClearFocus() end)  -- Close the edit box when pressing Escape

scrollFrame:SetScrollChild(editBox)  -- Make the edit box the scrollable content

-- Function to retrieve and list all items in bags and bank
local function GetAllItems()
    local items = {}  -- Table to store item names and their counts

    -- Function to scan a single container (bag or bank)
    local function ScanContainer(bag)
        local numSlots = C_Container.GetContainerNumSlots(bag)  -- Get the number of slots in the bag
        for slot = 1, numSlots do  -- Loop through all slots in the bag
            local itemLink = C_Container.GetContainerItemLink(bag, slot)  -- Get the item link for the item in the slot
            local itemInfo = C_Container.GetContainerItemInfo(bag, slot)  -- Get detailed info about the item

            if itemInfo and itemLink then  -- If the item exists and is valid
                local itemName = GetItemInfo(itemLink)  -- Get the item name from the link
                local itemCount = itemInfo.stackCount or 1  -- Get the count of the item in the stack (default 1)

                if itemName then  -- If the item has a valid name
                    -- Add the item count to the items table (if item already exists, add to the current count)
                    items[itemName] = (items[itemName] or 0) + itemCount
                end
            end
        end
    end

    -- Scan all personal inventory bags (backpack = 0, bags = 1-4)
    for bag = 0, 4 do
        ScanContainer(bag)  -- Scan each personal bag (main backpack and other bags)
    end

    -- Scan all bank bags (main bank = -1, bank bags = 5-11)
    -- Make sure to scan all bags including main bank and bank bags
    ScanContainer(BANK_CONTAINER)  -- Scan the main bank bag (-1)
    for bag = NUM_BANKBAGSLOTS, NUM_BANKBAGSLOTS + 4 do
        ScanContainer(bag)  -- Scan each additional bank bag (bags 5-11)
    end

    -- Convert the table of items into a string suitable for copying
    local result = ""
    -- Create a sorted list of item names
    local sortedItems = {}
    for itemName in pairs(items) do
        table.insert(sortedItems, itemName)  -- Insert item names into a new table
    end
    table.sort(sortedItems)  -- Sort the list of item names alphabetically

    -- Build the result string using the sorted item names
    for _, itemName in ipairs(sortedItems) do
        result = result .. itemName .. " x" .. items[itemName] .. "\n"  -- Format each item as "ItemName xCount"
    end

    return result  -- Return the formatted string with all items and their counts
end

-- Function to update the edit box with the inventory data
local function UpdateInventoryText()
    editBox:SetText(GetAllItems())  -- Set the text of the edit box to the output of GetAllItems
    editBox:HighlightText()  -- Highlight the text for easier copying
end

-- Create a button in the bank frame that will trigger the scan when clicked
local bankButton = CreateFrame("Button", "InventoryRequestButton", BankFrame, "UIPanelButtonTemplate")
bankButton:SetSize(100, 30)  -- Set the size of the button
bankButton:SetPoint("TOPLEFT", BankFrame, "TOPLEFT", 10, -30)  -- Position the button inside the bank frame
bankButton:SetText("Scan Items")  -- Set the button text
bankButton:SetScript("OnClick", function()
    frame:Show()  -- Show the frame when the button is clicked
    UpdateInventoryText()  -- Update the text inside the frame with inventory data
end)

-- Command to open the addon via the slash command "/invreq"
SLASH_INVENTORYREQUEST1 = "/invreq"
SlashCmdList["INVENTORYREQUEST"] = function()
    frame:Show()  -- Show the frame when the slash command is used
    UpdateInventoryText()  -- Update the text inside the frame with inventory data
end
