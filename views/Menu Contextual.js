{
                        title:'Copy',
                        shortcut:'Ctrl + C',
                        onclick:function() {
                            alert('Copy');
                        }
                    },
                    {
                        type:'line'
                    },
                    {title: 'Sub context menu',
                    submenu: [
                        {
                            title:'Sub menu 1',
                            shortcut:'Ctrl + X',
                            onclick:function() {
                                alert('SubMenu 1-1');
                            }
                        },
                        {
                            title:'Sub menu 2',
                            disabled: true,
                            onclick:function() {
                                alert('SubMenu 1-2')
                            }
                        }],
                    }